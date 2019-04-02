import pytest
import requests
import json
from datetime import datetime
from test_data import Testtextserachpayload
from pytest_lib import config, add_device_tag, add_mso_tag

headers={"Content-Type":"application/json","Accept":"application/json"}

@pytest.mark.synthetic_tests_textsearch
@pytest.mark.parametrize('device_domain', config["device_domains"])
class Testtextsearchbynumbers(Testtextserachpayload):

	@staticmethod
	def get_device_config(request, record_xml_attribute, device_domain):
		device_config = config["device_domain_config"][device_domain]
		add_mso_tag(
            request=request,
            record_xml_attribute=record_xml_attribute,
            mso=device_config['mso']
        )
		return device_config
	
	@pytest.mark.dependency()
	def test_searchcollection(self,device_domain, request, record_xml_attribute):
		device_domain_config = self.get_device_config(request, record_xml_attribute, device_domain)
		url=self.generate_textsearch_url(device_domain_config=device_domain_config)
		payload=self.textsearch_collection_payload(device_domain_config=device_domain_config)
		params=self.textsearch_params(device_domain_config=device_domain_config)
		response=requests.post(url=url,headers=headers,params=params,data=payload)
		assert response.status_code == 200
		try:
			json_data = json.loads(response.text)
			if "unifiedItem"  not in json_data:
				assert False,"The unifiedItem section is not present in the response of search collection api"
			else:
				if "collection" != json_data["unifiedItem"][0]["type"]:
					assert False,"The text collection is not present in the response of search collection api"
		except json.JSONDecodeError:
			assert False, "Decoding JSON from the response failed"
		except KeyError as e:
                        assert False, "Missing key while parsing the json response. Details:" + str(e)

	@pytest.mark.dependency()
	def test_searchcontent(self,device_domain, request, record_xml_attribute):
		device_domain_config = self.get_device_config(request, record_xml_attribute, device_domain)
		url=self.generate_textsearch_url(device_domain_config=device_domain_config)
		payload=self.textsearch_content_payload(device_domain_config=device_domain_config)
		params=self.textsearch_params(device_domain_config=device_domain_config)
		response=requests.post(url=url,headers=headers,params=params,data=payload)
		assert response.status_code == 200
		try:
			json_data = json.loads(response.text)
			if "unifiedItem"  not in json_data:
				assert False,"The unifiedItem section is not present in the response of search content api"
			else:
				if "content" != json_data["unifiedItem"][0]["type"]:
					assert False,"The text content is not present in the response of search content api"
		except json.JSONDecodeError:
			assert False, "Decoding JSON from the response failed"
		except KeyError as e:
                        assert False, "Missing key while parsing the json response. Details:" + str(e)

	@pytest.mark.dependency()
	def test_searchperson(self,device_domain, request, record_xml_attribute):
		device_domain_config = self.get_device_config(request, record_xml_attribute, device_domain)
		url=self.generate_textsearch_url(device_domain_config=device_domain_config)
		payload=self.textsearch_person_payload(device_domain_config=device_domain_config)
		params=self.textsearch_params(device_domain_config=device_domain_config)
		response=requests.post(url=url,headers=headers,params=params,data=payload)
		assert response.status_code == 200
		try:
			json_data = json.loads(response.text)
			if "unifiedItem"  not in json_data:
				assert False,"The unifiedItem section is not present in the response of search person api"
			else:
				if "person" != json_data["unifiedItem"][0]["type"]:
					assert False,"The text person is not present in the response of search person api"
		except json.JSONDecodeError:
			assert False, "Decoding JSON from the response failed"
		except KeyError as e:
                        assert False, "Missing key while parsing the json response. Details:" + str(e)

	@pytest.mark.dependency()
	def test_searchteam(self,device_domain, request, record_xml_attribute):
	    device_domain_config = self.get_device_config(request, record_xml_attribute, device_domain)
	    url=self.generate_textsearch_url(device_domain_config=device_domain_config)
	    payload=self.textsearch_team_payload(device_domain_config=device_domain_config)
	    params=self.textsearch_params(device_domain_config=device_domain_config)
	    response=requests.post(url=url,headers=headers,params=params,data=payload)
	    assert response.status_code == 200
	    try:
	    	json_data = json.loads(response.text)
	    	if "unifiedItem"  not in json_data:
	    		assert False,"The unifiedItem section is not present in the response of search team api"
	    	else:
	    		if "team" != json_data["unifiedItem"][0]["type"]:
	    			assert False,"The text team is not present in the response of search team api"
	    except json.JSONDecodeError:
	    	assert False, "Decoding JSON from the response failed"
	    except KeyError as e:
	    	assert False, "Missing key while parsing the json response. Details:" + str(e)

	@pytest.mark.dependency()
	def test_searchchannel(self,device_domain, request, record_xml_attribute):
		device_domain_config = self.get_device_config(request, record_xml_attribute, device_domain)
		url=self.generate_textsearch_url(device_domain_config=device_domain_config)
		payload=self.textsearch_channel_payload(device_domain_config=device_domain_config)
		params=self.textsearch_params(device_domain_config=device_domain_config)
		response=requests.post(url=url,headers=headers,params=params,data=payload)
		assert response.status_code == 200
		try:
			json_data = json.loads(response.text)
			if "unifiedItem"  not in json_data:
				assert False,"The unifiedItem section is not present in the response of search channel api"
			else:
				if "channel" != json_data["unifiedItem"][0]["type"]:
					assert False,"The text channel is not present in the response of search channel api"
		except json.JSONDecodeError:
			assert False, "Decoding JSON from the response failed"
		except KeyError as e:
                        assert False, "Missing key while parsing the json response. Details:" + str(e)
