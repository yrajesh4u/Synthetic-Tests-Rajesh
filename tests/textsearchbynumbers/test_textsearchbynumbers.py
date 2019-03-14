import pytest
import requests
import re
import json
from pytest_lib import config

headers = {"content-type": "application/json", "accept": "application/json"}
params = {"type":"discovery1NumericUnifiedItemSearch","bodyId":config['TextSearchBodyId_02']}
url='http://'+ config['MiddlemindVip'] + ':' + config['mm_port'] + '/' + config ["mind_version"]

class Testtextsearchbynumbers:

	def test_searchcollection(self):
		combined_payload=json.dumps({**config['payload'],**config['payload_collection']})
		response=requests.post(url=url,headers=headers,params=params,data=combined_payload)
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




	def test_searchcontent(self):
		combined_payload=json.dumps({**config['payload'],**config['payload_content']})
		response=requests.post(url=url,headers=headers,params=params,data=combined_payload)
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


	def test_searchperson(self):
		combined_payload=json.dumps({**config['payload'],**config['payload_person']})
		response=requests.post(url=url,headers=headers,params=params,data=combined_payload)
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

	def test_searchteam(self):
	    combined_payload=json.dumps({**config['payload'],**config['payload_team']})
	    response=requests.post(url=url,headers=headers,params=params,data=combined_payload)
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

	@pytest.mark.skip(reason="failing due to DS endpoint failure. TODO revisit later.")
	def test_searchchannel(self):
		combined_payload=json.dumps({**config['payload'],**config['payload_channel']})
		response=requests.post(url=url,headers=headers,params=params,data=combined_payload)
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



	

	
    

       
		


