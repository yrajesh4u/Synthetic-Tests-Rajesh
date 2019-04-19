import pytest
import requests
import json
from datetime import datetime
from test_data import Testtextserachpayload
from pytest_lib import config, add_device_tag, add_mso_tag
from synth_test_lib.synthassert import synthassert

headers={"Content-Type":"application/json","Accept":"application/json"}

@pytest.mark.synthetic_tests_textsearch
@pytest.mark.parametrize('device_domain', config["device_domains"])
class Testtextsearchbynumbers(Testtextserachpayload):
	@staticmethod
	def get_device_config(request, record_xml_attribute, device_domain):
		device_config = config["device_domain_config"][device_domain]
		add_device_tag(
			request=request,
			record_xml_attribute=record_xml_attribute,
			device=device_config['deviceType']
			)
		add_mso_tag(
			request=request,
			record_xml_attribute=record_xml_attribute,
			mso=device_config['mso']
			)
		return device_config
	
	@pytest.mark.dependency()
	def test_textsearch(self,device_domain, request, record_xml_attribute):
		device_domain_config = self.get_device_config(request, record_xml_attribute, device_domain)
		url=self.generate_textsearch_url(device_domain_config=device_domain_config)
		payload=self.textsearch_payload(device_domain_config=device_domain_config)
		params=self.textsearch_params(device_domain_config=device_domain_config)
		response=requests.post(url=url,headers=headers,params=params,data=payload)
		synthassert(response.status_code == 200,
					message=response.reason,
					response=response)
		try:
			json_data = json.loads(response.text)
			synthassert(
				"unifiedItem" in json_data,
				message=" Expected 'unifiedItem' in the response ",
				response=response)
			synthassert(
				json_data["unifiedItem"][0]["type"] == "collection" or "content" or "person" or "team" or "channel",
				message= "type validation failed:  Expected 'collection or content or person or team or channel' Actual '{}'".format(json_data["unifiedItem"][0]["type"]) ,
				response=response)					
		except json.JSONDecodeError:
			synthassert(False, 
						message="Decoding JSON from the response failed",
						response=response)
		except KeyError as e:
			synthassert(False, 
						message="Missing key while parsing the json response. Details:" + str(e),
				    	esponse=response)

	