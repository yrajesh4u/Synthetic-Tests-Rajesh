import pytest
import re
import json
import xmltodict
from envelopes import TestDataEnvelopes
from base import BodyUpdateService
from pytest_lib import config
import time

from synth_test_lib.synthassert import synthassert

class TestBodyUpdateServiceScenario1:
    testdata = TestDataEnvelopes()
    base = BodyUpdateService()

    def test_101_ProvAccountStore(self):
        url, method, data = self.testdata.data_ProvAccountStore()
        header = {'Content-Type': 'application/json'}
        resp = self.base.api_call(url, method, data, headers=header)
        resp_json = json.loads(resp.text)
        synthassert(bool(re.search('transactionId', resp.text)),
                    message='Not able to get transactionId in resp',
                    response=resp)
        synthassert(bool(re.search('optStatus', resp.text)),
                    message='Not able to get optStatus in resp',
                    response=resp)
        synthassert(resp_json['type'] == 'provAccount',
                    "Error:\nExpected 'provAccount'\nActual:  {}".format(resp_json['type']),
                    response=resp)

    def test_102_ProvDeviceActivate(self):
        url, method, data = self.testdata.data_ProvDeviceActivate()
        header = {'Content-Type': 'application/json'}
        resp = self.base.api_call(url, method, data, headers=header)
        resp_json = json.loads(resp.text)
        synthassert(resp_json['bodyId'],
                    message="bodyId not found",
                    response=resp)
        self.testdata.npvr_bodyId = resp_json['bodyId']
        synthassert(bool(re.search('transactionId', resp.text)), 
                    message='Not able to get transactionId in resp',
                    response=resp)
        synthassert(bool(re.search('deviceAlaCarteFeatureAttributeValue', resp.text)), 
                    'Not able to get optStatus in resp',
                    response=resp)
        synthassert(resp_json['serviceState'] == 'active', 
                    message="Error:\nExpected service state == 'active'\nActual '{}'".format(resp_json['serviceState']),
                    response=resp)
        
        time.sleep(30)

    def test_103_anonymizerPartnerExternalIdTranslate(self):
        url, method, data = self.testdata.data_anonymizerPartnerExternalIdTranslate()
        header = {'Content-Type': 'application/json'}
        resp = self.base.api_call(url, method, data, headers=header)
        resp_json = json.loads(resp.text)
        synthassert(resp_json['type'] == "anonymizerPartnerMap",
                    message="Error:\nExpected type == 'anonymizerPartnerMap\nActual:  '{}'".format(resp_json['type']),
                    response=resp)
        synthassert(resp_json['idType'] == config['idType'],
                    message="Error:\nExpected '{}'\nActual:  '{}'",
                    response=resp)
        synthassert(resp_json['partnerId'] == "tivo:pt.3689",
                    message="Error:\nExpected:  'tivo:pt.3689'\nActual:  '{}'".format(resp_json['partnerId']),
                    response=resp)
        synthassert(bool(re.search('internalId', resp.text)), 
                    message="Not able to get internalId in resp",
                    response=resp)
        self.testdata.internalId = resp_json['internalId']

    def test_104_npvrEnablementSearch(self):
        url, method, data = self.testdata.data_npvrEnablementSearch()
        header = {'Content-Type': 'application/json'}
        resp = self.base.api_call(url, method, data, headers=header)
        resp_json = json.loads(resp.text)
        synthassert(bool(re.search('npvrEnablement', resp.text)), 
                    message="Not able to get npvrEnablement in resp",
                    response=resp)
        synthassert(resp_json['type'] == 'npvrEnablementList',
                    message="Error:\nExpected type == 'npvrEnablementList'\nActual:  '{}'".format(resp_json['type']),
                    response=resp)
        synthassert(resp_json['npvrEnablement'][0]['npvrEnabled'],
                    message="Error: npvrEnabled is not true",
                    response=resp)
        time.sleep(10)

    def test_105_tveServiceActivate(self):
        url, method, data = self.testdata.data_tveServiceActivate()
        header = {'Content-Type': 'text/xml', 'Accept': '*/*'}
        cert = ('./3767.crt', './3767.key')
        resp = self.base.api_call(url, method, data, headers=header, cert=cert, verify=False, timeout=150)
        resp_json = xmltodict.parse(resp.text)
        synthassert(bool(re.search('tveServiceActivateResponse', resp.text)), 
                    message="No tveServiceActivateResponse in resp",
                    response=resp)
        synthassert(bool(re.search('tivoSerialNumber', resp.text)),
                    message='No tivoSerialNumber in resp',
                    response=resp)
        self.testdata.bodyId = resp_json['tveServiceActivateResponse']['tivoSerialNumber']
        synthassert(resp_json['tveServiceActivateResponse']['status'] == 'success', 
                    message="Error:\nExpected status == 'sucess'\nActual:  '{}'".format(resp_json['tveServiceActivateResponse']['status']),
                    response=resp)
        time.sleep(60)

    def test_106_npvrEnablementSearchAfterAddingDevice(self):
        url, method, data = self.testdata.data_npvrEnablementSearch()
        header = {'Content-Type': 'application/json'}
        resp = self.base.api_call(url, method, data, headers=header)
        resp_json = json.loads(resp.text)
        synthassert(bool(re.search('npvrEnablement', resp.text)), 
                    message='Not able to get npvrEnablement in resp',
                    response=resp)
        synthassert(resp_json['type'] == 'npvrEnablementList', 
                    message="Error:\nExpected type == npvrEnablementList'\nActual:  '{}'".format(resp_json['type']),
                    response=resp)
        synthassert(resp_json['npvrEnablement'][0]['npvrEnabled'],
                    message='Error: npvrEnabled is not true', 
                    response=resp)
        time.sleep(10)

    def test_107_bodyConfigSearch(self):
        url, method, data = self.testdata.data_bodyConfigSearch()
        header = {'Content-Type': 'application/json'}
        resp = self.base.api_call(url, method, data, headers=header)
        synthassert(bool(re.search('networkPvr', resp.text)),
                    message='Not able to get networkPvr in resp',
                    response=resp)
        synthassert(bool(re.search('bodyConfigList', resp.text)),
                    message='Not able to get bodyConfigList in resp',
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
        synthassert(resp_json['type'] == 'success', 
                    message="Error:\nExpected type == 'success\nActual:  '{}'".format(resp_json['type']),
                    response=resp)
        time.sleep(30)

    def test_109_bodyConfigSearchAfterCancel(self):
        url, method, data = self.testdata.data_bodyConfigSearch()
        header = {'Content-Type': 'application/json'}
        resp = self.base.api_call(url, method, data, headers=header)
        synthassert(not(bool(re.search('networkPvr', resp.text))), 
                    message='Able to get networkPvr in resp',
                    response=resp)
        synthassert(bool(re.search('bodyConfigList', resp.text)), 
                    message='Not able to get bodyConfigList in resp',
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
        synthassert(bool(re.search('tveServiceCancelResponse', resp.text)), 
                    message='No tveServiceActivateResponse in resp',
                    response=resp)
        synthassert(resp_json['tveServiceCancelResponse']['status'] == 'success',
                    message="Error:\nExpected status == 'success'\nActual:  '{}'".format(resp_json['tveServiceCancelResponse']['status']),
                    response=resp)



