import pytest
import re
import json
import xmltodict
from envelopes import TestDataEnvelopes
from base import BodyUpdateService
from pytest_lib import config
import time


class TestBodyUpdateServiceScenario2:
    testdata = TestDataEnvelopes()
    base = BodyUpdateService()


    def test_101_tveServiceActivate(self):
        url, method, data = self.testdata.data_tveServiceActivate()
        header = {'Content-Type': 'text/xml', 'Accept': '*/*'}
        cert = ('./3767.crt', './3767.key')
        resp = self.base.api_call(url, method, data, headers=header, cert=cert, verify=False, timeout=150)
        resp_json = xmltodict.parse(resp.text)
        self.testdata.bodyId = resp_json['tveServiceActivateResponse']['tivoSerialNumber']
        assert bool(re.search('tveServiceActivateResponse', resp.text)), 'No tveServiceActivateResponse in resp'
        assert bool(re.search('tivoSerialNumber', resp.text)), 'No tivoSerialNumber in resp'
        assert resp_json['tveServiceActivateResponse']['status'] == 'success', 'Error: status != success'
        time.sleep(60)

    def test_102_anonymizerPartnerExternalIdTranslate(self):
        url, method, data = self.testdata.data_anonymizerPartnerExternalIdTranslate()
        header = {'Content-Type': 'application/json'}
        resp = self.base.api_call(url, method, data, headers=header)
        resp_json = json.loads(resp.text)
        self.testdata.internalId = resp_json['internalId']
        assert resp_json['type'] == "anonymizerPartnerMap", 'Error: type not Matching'
        assert resp_json['idType'] == config['idType'], 'Error: idType not Matching.'
        assert resp_json['partnerId'] == "tivo:pt.3689", 'Error: partnerId not Matching.'
        assert bool(re.search('internalId', resp.text)), 'Not able to get internalId in resp'

    def test_103_npvrEnablementSearch(self):
        url, method, data = self.testdata.data_npvrEnablementSearch()
        header = {'Content-Type': 'application/json'}
        resp = self.base.api_call(url, method, data, headers=header)
        resp_json = json.loads(resp.text)
        assert bool(re.search('npvrEnablement', resp.text)), 'Not able to get npvrEnablement in resp'
        assert resp_json['type'] == 'npvrEnablementList', 'Error: type not found.'
        assert not (resp_json['npvrEnablement'][0]['npvrEnabled']), 'Error: npvrEnabled is true'
        time.sleep(5)

    def test_104_bodyConfigSearch(self):
        url, method, data = self.testdata.data_bodyConfigSearch()
        header = {'Content-Type': 'application/json'}
        resp = self.base.api_call(url, method, data, headers=header)
        resp_json = json.loads(resp.text)
        assert not (bool(re.search('networkPvr', resp.text))), 'Able to get networkPvr in resp'
        assert bool(re.search('bodyConfigList', resp.text)), 'Not able to get bodyConfigList in resp'
        assert bool(re.search('recordingSettings', resp.text)), 'Not able to get recordingSettings in resp'
        time.sleep(5)

    def test_105_ProvDeviceActivate(self):
        url, method, data = self.testdata.data_ProvDeviceActivate()
        header = {'Content-Type': 'application/json'}
        resp = self.base.api_call(url, method, data, headers=header)
        resp_json = json.loads(resp.text)
        self.testdata.npvr_bodyId = resp_json['bodyId']
        assert bool(re.search('transactionId', resp.text)), 'Not able to get transactionId in resp'
        assert bool(re.search('deviceAlaCarteFeatureAttributeValue', resp.text)), 'Not able to get optStatus in resp'
        assert resp_json['serviceState'] == 'active', 'Error: serviceState not found.'
        time.sleep(60)

    def test_106_npvrEnablementSearchAfterAddingDevice(self):
        url, method, data = self.testdata.data_npvrEnablementSearch()
        header = {'Content-Type': 'application/json'}
        resp = self.base.api_call(url, method, data, headers=header)
        resp_json = json.loads(resp.text)
        assert bool(re.search('npvrEnablement', resp.text)), 'Not able to get npvrEnablement in resp'
        assert resp_json['type'] == 'npvrEnablementList', 'Error: type not found.'
        assert resp_json['npvrEnablement'][0]['npvrEnabled'], 'Error: npvrEnabled is not true'
        time.sleep(5)

    def test_107_bodyConfigSearch(self):
        url, method, data = self.testdata.data_bodyConfigSearch()
        header = {'Content-Type': 'application/json'}
        resp = self.base.api_call(url, method, data, headers=header)
        resp_json = json.loads(resp.text)
        assert bool(re.search('networkPvr', resp.text)), 'Not able to get networkPvr in resp'
        assert bool(re.search('bodyConfigList', resp.text)), 'Not able to get bodyConfigList in resp'
        assert bool(re.search('recordingSettings', resp.text)), 'Not able to get recordingSettings in resp'
        #add more
        time.sleep(5)

    def test_108_ProvDeviceCancel(self):
        url, method, data = self.testdata.data_pr1ProvDeviceCancel()
        header = {'Content-Type': 'application/json'}
        resp = self.base.api_call(url, method, data, headers=header)
        resp_json = json.loads(resp.text)
        assert resp_json['type'] == 'success', 'Error: type!=success'
        time.sleep(60)

    def test_109_bodyConfigSearchAfterCancel(self):
        url, method, data = self.testdata.data_bodyConfigSearch()
        header = {'Content-Type': 'application/json'}
        resp = self.base.api_call(url, method, data, headers=header)
        resp_json = json.loads(resp.text)
        assert not(bool(re.search('networkPvr', resp.text))), 'Able to get networkPvr in resp'
        assert bool(re.search('bodyConfigList', resp.text)), 'Not able to get bodyConfigList in resp'
        assert bool(re.search('recordingSettings', resp.text)), 'Not able to get recordingSettings in resp'
        time.sleep(5)

    def test_110_tveServiceCancel(self):
        url, method, data = self.testdata.data_tveServiceCancel()
        header = {'Content-Type': 'text/xml', 'Accept': '*/*'}
        cert = ('./3767.crt', './3767.key')
        resp = self.base.api_call(url, method, data, headers=header, cert=cert, verify=False, timeout=150)
        resp_json = xmltodict.parse(resp.text)
        assert bool(re.search('tveServiceCancelResponse', resp.text)), 'No tveServiceActivateResponse in resp'
        assert resp_json['tveServiceCancelResponse']['status'] == 'success', 'Error: status != success'



