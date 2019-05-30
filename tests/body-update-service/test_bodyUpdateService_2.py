import pytest
import re
import json
import xmltodict
from envelopes import TestDataEnvelopes
from base import BodyUpdateService
from pytest_lib import config
import time
from synth_test_lib.synthassert import synthassert


class TestBodyUpdateServiceScenario2:
    testdata = TestDataEnvelopes()
    base = BodyUpdateService()

    def test_101_tveServiceActivate(self):
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
                    message="Error:\nExpected status == 'sucess'\nActual:  '{}'".format(
                        resp_json['tveServiceActivateResponse']['status']),
                    response=resp)

        self.testdata.bodyId = resp_json['tveServiceActivateResponse']['tivoSerialNumber']
        self.testdata.tveServiceActivate_requestId = resp_json['tveServiceActivateResponse']['requestId']

    def test_101_tveServiceActivate_kafka_log(self, tve_service_activate_kafka_consumer):
        status, tivo_customer_id = \
            self.base.tve_service_activate_kafka_validation(tve_service_activate_kafka_consumer,
                                                            self.testdata.tveServiceActivate_requestId)
        # Added 3 min sleep after tveServiceActivate and kafka log capture.
        time.sleep(180)
        assert status, tivo_customer_id
        self.testdata.tivo_customer_id = tivo_customer_id

    def test_102_anonymizerPartnerExternalIdTranslate(self):
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
        synthassert(self.testdata.tivo_customer_id == resp_json['internalId'],
                    message="Error tivo_customer_id in KafkaLog != internalId in anonymizerPartnerExternalIdTranslate:"
                            "\nExpected: %s \nActual: %s" % (self.testdata.tivo_customer_id, resp_json['internalId']),
                    response=resp)

        self.testdata.internalId = resp_json['internalId']


    def test_103_npvrEnablementSearch(self):
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
        synthassert(not (resp_json['npvrEnablement'][0]['npvrEnabled']),
                    message="Error: npvrEnabled is true",
                    response=resp)

        time.sleep(10)

    def test_104_bodyConfigSearch(self):
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
        synthassert(not (bool(re.search('networkPvr', resp.text))),
                    message='Able to get networkPvr in resp',
                    response=resp)
        synthassert(bool(re.search('recordingSettings', resp.text)),
                    message='Not able to get recordingSettings in resp',
                    response=resp)

        time.sleep(5)

    def test_105_ProvDeviceActivate(self):
        url, method, data = self.testdata.data_ProvDeviceActivate()
        header = {'Content-Type': 'application/json'}
        resp = self.base.api_call(url, method, data, headers=header)
        resp_json = json.loads(resp.text)


        synthassert('bodyId' in resp_json,
                    message="bodyId not available in response json",
                    response=resp)
        synthassert('transactionId' in resp_json,
                    message='Not able to get "transactionId" in resp',
                    response=resp)
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

        self.testdata.npvr_bodyId = resp_json['bodyId']
        time.sleep(180)

    def test_106_npvrEnablementSearchAfterAddingDevice(self):
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

        time.sleep(5)

    def test_107_bodyConfigSearch(self):
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

        time.sleep(5)

    def test_108_ProvDeviceCancel(self):
        url, method, data = self.testdata.data_pr1ProvDeviceCancel()
        header = {'Content-Type': 'application/json'}
        resp = self.base.api_call(url, method, data, headers=header)
        resp_json = json.loads(resp.text)

        synthassert('type' in resp_json,
                    'Not able to get "type" in resp',
                    response=resp)
        synthassert(resp_json['type'] == 'success',
                    message="Error:\nExpected type == 'success'\nActual:  '{}'".format(resp_json['type']),
                    response=resp)

        time.sleep(180)

    def test_109_bodyConfigSearchAfterCancel(self):
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

        time.sleep(5)

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

        time.sleep(180)
