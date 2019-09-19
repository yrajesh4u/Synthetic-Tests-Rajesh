import pytest
import json
from envelopes import TestDataEnvelopes
from base import BodyUpdateService
from pytest_lib import config, mso_tag
from synth_test_lib.synthassert import synthassert

@pytest.mark.parametrize('mso', ['common'])
@pytest.mark.usefixtures("mso_tag")
class TestBodyUpdateServiceHealthInfo:
    ```
    TITLE: Health of bodyUpdateService
    DESCRIPTION: 
    This is to validate if bodyUpdateService is up and running. It checks for health and info endpoints
    
    ```    
        
    testdata = TestDataEnvelopes()
    base = BodyUpdateService()

    @pytest.mark.parametrize("node", config['app_node'])
    def test_100_app_health(self, node):
        url, method, data = self.testdata.data_get_health(node)
        resp = self.base.api_call(url, method, data)
        resp_json = json.loads(resp.text)
        synthassert('status' in resp_json,
                    message="Error, Not able to find status in resp_json=%s" % resp.text,
                    response=resp)
        synthassert(resp_json['status'] == 'UP',
                    message="Error:\nExpected status == 'UP'\nActual:  '{}'".format(
                        resp_json['status']),
                    response=resp)

    @pytest.mark.parametrize("node", config['app_node'])
    def test_100_app_info(self, node):
        url, method, data = self.testdata.data_get_info(node)
        resp = self.base.api_call(url, method, data)
        resp_json = json.loads(resp.text)
        synthassert('properties' in resp_json,
                    message="Error, Not able to find properties in resp_json=%s" % resp.text,
                    response=resp)

        synthassert('appname' in resp_json['properties'],
                    message="Error, Not able to find appname in resp_json=%s" % resp.text,
                    response=resp)
        synthassert(resp_json['properties']['appname'] == 'bodyUpdateService',
                    message="Error:\nExpected appname == 'bodyUpdateService'\nActual:  '{}'".format(
                        resp_json['properties']['appname']),
                    response=resp)
