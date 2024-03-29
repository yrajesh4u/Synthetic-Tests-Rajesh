import pytest
import re
import json
import xmltodict
from envelopes import TestDataEnvelopes
from base import BodyUpdateService
from pytest_lib import config, mso_tag
import time
from synth_test_lib.synthassert import synthassert

@pytest.mark.parametrize('mso', ['common'])
@pytest.mark.usefixtures("mso_tag")
class TestBodyUpdateServiceScenario1:
    '''
    TITLE: Device Provision then nDVR Activation
    DESCRIPTION: 
    Activates a Streamer Body in an Account.
    Activates a nDVR device in the same Account.
    Tests if Body Update Service populates Network PVR field in the response of Body Config Search.
    '''
    testdata = TestDataEnvelopes()
    base = BodyUpdateService()


    def test_101_ProvAccountStore(self):
        pytest.skip('This test require only for new PCID')
        for elem in config['partnerCustomerList']:
            url, method, data = self.testdata.data_ProvAccountStore(elem)
            header = {'Content-Type': 'application/json'}
            resp = self.base.api_call(url, method, data, headers=header)

            resp_json = json.loads(resp.text)
            synthassert('transactionId' in resp_json,
                        message='Not able to get transactionId in resp',
                        response=resp)
            synthassert('optStatus' in resp_json,
                        message='Not able to get optStatus in resp',
                        response=resp)
            synthassert(resp_json['type'] == 'provAccount',
                        "Error:\nExpected 'provAccount'\nActual:  {}".format(resp_json['type']),
                        response=resp)
            synthassert('partnerAccount' in resp_json,
                        message='Not able to get partnerAccount in resp',
                        response=resp)
            synthassert('partnerCustomerId' in resp_json['partnerAccount'],
                        message='Not able to get partnerCustomerId in resp',
                        response=resp)
            synthassert(str(resp_json['partnerAccount']['partnerCustomerId']) == str(elem),
                        message="Error:\nExpected {} \nActual:  {}".format(
                            elem,
                            resp_json['partnerAccount']['partnerCustomerId']),
                        response=resp)

    def test_102_ProvDeviceActivate(self, prov_device_kafka_consumer, tve_service_kafka_consumer):
        url, method, data = self.testdata.data_ProvDeviceActivate()
        header = {'Content-Type': 'application/json'}
        resp = self.base.api_call(url, method, data, headers=header)
        resp_json = json.loads(resp.text)

        if 'bodyId' in resp_json:
            self.testdata.npvr_bodyId = resp_json['bodyId']
            synthassert('transactionId' in resp_json,
                        message='Not able to get "transactionId" in resp',
                        response=resp)

            self.testdata.ProvDeviceActivate_txnId = resp_json['transactionId']
            synthassert('type' in resp_json,
                        message='Not able to get "type" in resp',
                        response=resp)
            synthassert('serviceState' in resp_json,
                        message='Not able to get "serviceState" in resp',
                        response=resp)
            synthassert('deviceAlaCarteFeatureAttributeValue' in resp_json,
                        'Not able to get "deviceAlaCarteFeatureAttributeValue" in resp',
                        response=resp)
            synthassert(resp_json['serviceState'] == 'active',
                        message="Error:\nExpected service state == 'active'\nActual '{}'".format(resp_json['serviceState']),
                        response=resp)
            synthassert(resp_json['type'] == 'provDevice',
                        message="Error:\nExpected type == 'provDevice'\nActual '{}'".format(resp_json['type']),
                        response=resp)

        elif resp_json['code'] == 'badArgument':
            try:
                self.testdata.npvr_bodyId = re.search('.*has an active nPVR device: (tsn:.*) associated to it.*',
                                                      resp_json['text']).group(1)
                self.testdata.ProvDeviceActivate_txnId = None
                self.testdata.usingExisingNpvrBodyId = True
                print(self.testdata.npvr_bodyId, self.testdata.usingExisingNpvrBodyId)
            except AttributeError:
                synthassert(False,
                            message="bodyId Or badArgument not available in response json",
                            response=resp)
        else:
            synthassert('bodyId' in resp_json,
                        message="bodyId not available in response json",
                        response=resp)

    def test_102_ProvDeviceActivate_kafka_log(self, prov_device_kafka_consumer):
        if self.testdata.usingExisingNpvrBodyId:
            pytest.skip("Using existing NPVR device.")

        status, service_fe_account_id = \
            self.base.prov_device_activate_kafka_validation(prov_device_kafka_consumer,
                                                            self.testdata.ProvDeviceActivate_txnId)
        time.sleep(250)
        assert status, service_fe_account_id
        self.testdata.service_fe_account_id = service_fe_account_id

    def test_103_anonymizerPartnerExternalIdTranslate(self):
        url, method, data = self.testdata.data_anonymizerPartnerExternalIdTranslate()
        header = {'Content-Type': 'application/json'}
        resp = self.base.api_call(url, method, data, headers=header)

        resp_json = json.loads(resp.text)
        synthassert('externalId' in resp_json,
                    'Not able to get "externalId" in resp',
                    response=resp)
        synthassert('idType' in resp_json,
                    'Not able to get "idType" in resp',
                    response=resp)
        synthassert('internalId' in resp_json,
                    'Not able to get "internalId" in resp',
                    response=resp)
        self.testdata.internalId = resp_json['internalId']
        synthassert('partnerExternalId' in resp_json,
                    'Not able to get "partnerExternalId" in resp',
                    response=resp)
        synthassert('type' in resp_json,
                    'Not able to get "type" in resp',
                    response=resp)
        synthassert(resp_json['type'] == "anonymizerPartnerMap",
                    message="Error:\nExpected type == 'anonymizerPartnerMap\nActual:  '{}'".format(resp_json['type']),
                    response=resp)
        synthassert(resp_json['idType'] == config['idType'],
                    message="Error:\nExpected '{}'\nActual:  '{}'".format(config['idType'], resp_json['idType']),
                    response=resp)
        synthassert(resp_json['partnerId'] == "tivo:pt.3689",
                    message="Error:\nExpected:  'tivo:pt.3689'\nActual:  '{}'".format(resp_json['partnerId']),
                    response=resp)

        if self.testdata.usingExisingNpvrBodyId:
            self.testdata.service_fe_account_id = resp_json['internalId']
        else:
            synthassert(self.testdata.service_fe_account_id == resp_json['internalId'],
                        message="Error service_fe_account_id in KafkaLog != internalId in "
                                "anonymizerPartnerExternalIdTranslate\nExpected: %s \nActual: %s"
                                % (self.testdata.service_fe_account_id, resp_json['internalId']),
                        response=resp)

    def test_104_npvrEnablementSearch(self):
        url, method, data = self.testdata.data_npvrEnablementSearch()
        header = {'Content-Type': 'application/json'}
        resp = self.base.api_call(url, method, data, headers=header)
        resp_json = json.loads(resp.text)

        synthassert('npvrEnablement' in resp_json,
                    'Not able to get "npvrEnablement" in resp',
                    response=resp)
        synthassert('type' in resp_json,
                    'Not able to get "type" in resp',
                    response=resp)
        synthassert(resp_json['type'] == 'npvrEnablementList',
                    message="Error:\nExpected type == 'npvrEnablementList'\nActual:  '{}'".format(resp_json['type']),
                    response=resp)
        synthassert(resp_json['npvrEnablement'][0]['npvrEnabled'],
                    message="Error: npvrEnabled is not true",
                    response=resp)

        time.sleep(10)

    def test_105_tveServiceActivate(self):
        if self.testdata.usingExisingNpvrBodyId:
            pytest.skip("Using existing NPVR device.")

        url, method, data = self.testdata.data_tveServiceActivate()
        header = {'Content-Type': 'text/xml', 'Accept': '*/*'}
        cert = ('./3767.crt', './3767.key')
        resp = self.base.api_call(url, method, data, headers=header, cert=cert, verify=False, timeout=150)
        resp_json = xmltodict.parse(resp.text)

        synthassert('tveServiceActivateResponse' in resp_json,
                    'Not able to get "tveServiceActivateResponse" in resp',
                    response=resp)
        synthassert('requestId' in resp_json['tveServiceActivateResponse'],
                    'Not able to get "requestId" in resp',
                    response=resp)
        synthassert('status' in resp_json['tveServiceActivateResponse'],
                    'Not able to get "status" in resp',
                    response=resp)
        synthassert('tivoSerialNumber' in resp_json['tveServiceActivateResponse'],
                    'Not able to get "tivoSerialNumber" in resp',
                    response=resp)
        synthassert(resp_json['tveServiceActivateResponse']['status'] == 'success',
                    message="Error:\nExpected status == 'success'\nActual:  '{}'".format(
                        resp_json['tveServiceActivateResponse']['status']),
                    response=resp)

        self.testdata.bodyId = resp_json['tveServiceActivateResponse']['tivoSerialNumber']
        self.testdata.tveServiceActivate_requestId = resp_json['tveServiceActivateResponse']['requestId']

    def test_105_tveServiceActivate_kafka_log(self, tve_service_kafka_consumer):
        if self.testdata.usingExisingNpvrBodyId:
            pytest.skip("Using existing NPVR device.")

        self.testdata.tve_activate_status, tivo_customer_id = \
            self.base.tve_service_activate_kafka_validation(tve_service_kafka_consumer,
                                                            self.testdata.tveServiceActivate_requestId)

        assert self.testdata.tve_activate_status, tivo_customer_id
        self.testdata.tivo_customer_id = tivo_customer_id

    def test_106_npvrEnablementSearchAfterAddingDevice(self):
        if self.testdata.usingExisingNpvrBodyId:
            pytest.skip("Dependent: test_105_tveServiceActivate_kafka_log. bypassing to cancel.")

        url, method, data = self.testdata.data_npvrEnablementSearch()
        header = {'Content-Type': 'application/json'}
        resp = self.base.api_call(url, method, data, headers=header)

        resp_json = json.loads(resp.text)
        synthassert('npvrEnablement' in resp_json,
                    'Not able to get "npvrEnablement" in resp',
                    response=resp)
        synthassert('type' in resp_json,
                    'Not able to get "type" in resp',
                    response=resp)
        synthassert(resp_json['type'] == 'npvrEnablementList',
                    message="Error:\nExpected type == npvrEnablementList'\nActual:  '{}'".format(resp_json['type']),
                    response=resp)
        synthassert(resp_json['npvrEnablement'][0]['npvrEnabled'],
                    message='Error: npvrEnabled is not true',
                    response=resp)

        time.sleep(10)

    def test_107_bodyConfigSearch(self):
        if self.testdata.usingExisingNpvrBodyId:
            pytest.skip("Dependent: test_105_tveServiceActivate_kafka_log. bypassing to cancel.")

        url, method, data = self.testdata.data_bodyConfigSearch()
        header = {'Content-Type': 'application/json'}
        resp = self.base.api_call(url, method, data, headers=header)

        resp_json = json.loads(resp.text)
        synthassert('bodyConfig' in resp_json,
                    'Not able to get "bodyConfig" in resp',
                    response=resp)
        synthassert('type' in resp_json,
                    'Not able to get "type" in resp',
                    response=resp)
        synthassert(resp_json['type'] == 'bodyConfigList',
                    message="Error:\nExpected type == bodyConfigList'\nActual:  '{}'".format(resp_json['type']),
                    response=resp)
        synthassert(bool(re.search('networkPvr', resp.text)),
                    message='Not able to get networkPvr in resp',
                    response=resp)
        synthassert(bool(re.search('recordingSettings', resp.text)),
                    message='Not able to get recordingSettings in resp',
                    response=resp)

        time.sleep(10)

    def test_108_ProvDeviceCancel(self):
        url, method, data = self.testdata.data_pr1ProvDeviceCancel()
        header = {'Content-Type': 'application/json'}
        resp = self.base.api_call(url, method, data, headers=header)

        resp_json = json.loads(resp.text)
        synthassert('type' in resp_json,
                    'Not able to get "type" in resp',
                    response=resp)
        synthassert(resp_json['type'] == 'success',
                    message="Error:\nExpected type == 'success\nActual:  '{}'".format(resp_json['type']),
                    response=resp)

    def test_108_ProvDeviceCancel_kafka_log(self, prov_device_kafka_consumer):
        service_state = \
            self.base.prov_device_cancle_kafka_validation(prov_device_kafka_consumer,
                                                          self.testdata.service_fe_account_id)

        assert service_state, 'Not able to find serviceState=cancel for given serviceFeAccountId=%s' % \
                              self.testdata.service_fe_account_id
        time.sleep(250)

    def test_109_bodyConfigSearchAfterCancel(self):
        if self.testdata.usingExisingNpvrBodyId:
            pytest.skip("tve service activate fail. bypassing to cancel.")

        url, method, data = self.testdata.data_bodyConfigSearch()
        header = {'Content-Type': 'application/json'}
        resp = self.base.api_call(url, method, data, headers=header)

        resp_json = json.loads(resp.text)
        synthassert(not (bool(re.search('networkPvr', resp.text))),
                    message='Able to get networkPvr in resp',
                    response=resp)
        synthassert('type' in resp_json,
                    'Not able to get "type" in resp',
                    response=resp)
        synthassert(resp_json['type'] == 'bodyConfigList',
                    message="Error:\nExpected type == bodyConfigList'\nActual:  '{}'".format(resp_json['type']),
                    response=resp)
        synthassert(bool(re.search('recordingSettings', resp.text)),
                    message='Not able to get recordingSettings in resp',
                    response=resp)

        time.sleep(10)

    def test_110_tveServiceCancel(self):
        url, method, data = self.testdata.data_tveServiceCancel()
        header = {'Content-Type': 'text/xml', 'Accept': '*/*'}
        cert = ('./3767.crt', './3767.key')
        resp = self.base.api_call(url, method, data, headers=header, cert=cert, verify=False, timeout=150)

        resp_json = xmltodict.parse(resp.text)
        synthassert('tveServiceCancelResponse' in resp_json,
                    'Not able to get "tveServiceCancelResponse" in resp',
                    response=resp)
        synthassert('requestId' in resp_json['tveServiceCancelResponse'],
                    'Not able to get "requestId" in resp',
                    response=resp)
        synthassert('status' in resp_json['tveServiceCancelResponse'],
                    'Not able to get "status" in resp',
                    response=resp)
        synthassert(resp_json['tveServiceCancelResponse']['status'] == 'success',
                    message="Error:\nExpected status == 'success'\nActual:  '{}'".format(
                        resp_json['tveServiceCancelResponse']['status']),
                    response=resp)


    def test_110_tveServiceCancel_kafka_log(self, tve_service_kafka_consumer):
        if self.testdata.usingExisingNpvrBodyId:
            pytest.skip("Dependent: test_105_tveServiceActivate_kafka_log. bypassing to cancel.")

        tivo_customer_id = \
            self.base.tve_service_cancel_kafka_validation(tve_service_kafka_consumer,
                                                          self.testdata.tivo_customer_id,
                                                          self.testdata.tveServiceActivate_requestId)
        assert tivo_customer_id, "tivo_customer_id cancel fail for given tivo_customer_id=%s" % \
                                 self.testdata.tivo_customer_id
