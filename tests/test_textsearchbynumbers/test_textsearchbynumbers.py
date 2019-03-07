import pytest
import requests
import re
import json
from pytest_lib import config

headers = {"content-type": "application/json", "accept": "application/json"}
params = {"type":"discovery1NumericUnifiedItemSearch","bodyId":config["TextSearchBodyId_02"]}
url='http://'+ config['MiddlemindVip'] + ':' + config['mm_port'] + '/' + config ["mind_version"]

class Testtextsearchbynumbers:

	def test_searchcollection(self):
		payload ='{ "numbers" : "22", "includePaid" : true, "numRelevantItems" : "100", "bodyId" :"' +  config["TextSearchBodyId_02"] +'",\
	    			"includeBroadband" : true,                           "includeIpVod" : true, "useLineup" : false, "offset" : "0",\
	    			"includePersonSearch" : true,                        "count" : "1", "includeBroadcast" : true, "includeFree" : true,\
	    			"includeVod" : true, "mergeOverridingCollections" : true, "minEndTime" : "2016-10-14 12:43:21", "mergeOverridingContent"\
	    			: true, "searchable" : true, "includeUnifiedItemType" : [ "collection" ], "orderBy" : [ "relevance", "strippedTitle" ],\
	    			"type" : "discovery1NumericUnifiedItemSearch"    }'
		response=requests.post(url,headers=headers,params=params,data=payload)
		assert re.search("collection",response.text)


	def test_searchcontent(self):
		payload ='{ "numbers" : "33", "includePaid" : true, "numRelevantItems" : "100", "bodyId" :"' + config["TextSearchBodyId_02"] +'",\
	    			"includeBroadband" : true,                           "includeIpVod" : true, "useLineup" : false, "offset" : "0",\
	    			"includePersonSearch" : true,                        "count" : "1", "includeBroadcast" : true, "includeFree" : true,\
	    			"includeVod" : true, "mergeOverridingCollections" : true, "minEndTime" : "2016-10-14 12:43:21", "mergeOverridingContent"\
	    			: true, "searchable" : true, "includeUnifiedItemType" : [ "content" ], "orderBy" : [ "relevance", "strippedTitle" ],\
	    			"type" : "discovery1NumericUnifiedItemSearch"    }'
		response=requests.post(url=url,headers=headers,params=params,data=payload)
		assert re.search("content",response.text)

	def test_searchperson(self):
		payload ='{ "numbers" : "44", "includePaid" : true, "numRelevantItems" : "100", "bodyId" :"' + config["TextSearchBodyId_02"] +'",\
	    			"includeBroadband" : true,                           "includeIpVod" : true, "useLineup" : false, "offset" : "0",\
	    			"includePersonSearch" : true,                        "count" : "2", "includeBroadcast" : true, "includeFree" : true,\
	    			"includeVod" : true, "mergeOverridingCollections" : true, "minEndTime" : "2016-10-14 12:43:21", "mergeOverridingContent"\
	    			: true, "searchable" : true, "includeUnifiedItemType" : [ "person" ], "orderBy" : [ "relevance", "strippedTitle" ],\
	    			"type" : "discovery1NumericUnifiedItemSearch"    }'
		response=requests.post(url=url,headers=headers,params=params,data=payload)
		assert re.search("person",response.text)

	def test_searchteam(self):
		payload ='{ "numbers" : "22", "includePaid" : true, "numRelevantItems" : "100", "bodyId" :"' + config["TextSearchBodyId_02"]+'",\
	    			"includeBroadband" : true,                           "includeIpVod" : true, "useLineup" : false, "offset" : "0",\
	    			"includePersonSearch" : true,                        "count" : "2", "includeBroadcast" : true, "includeFree" : true,\
	    			"includeVod" : true, "mergeOverridingCollections" : true, "minEndTime" : "2016-10-14 12:43:21", "mergeOverridingContent"\
	    			: true, "searchable" : true, "includeUnifiedItemType" : [ "team" ], "orderBy" : [ "relevance", "strippedTitle" ],\
	    			"type" : "discovery1NumericUnifiedItemSearch"    }'
		response=requests.post(url=url,headers=headers,params=params,data=payload)
		assert re.search("team",response.text)

	def test_searchchannel(self):
		payload ='{ "numbers" : "2222", "includePaid" : true, "numRelevantItems" : "100", "bodyId" :"' + config["TextSearchBodyId_02"]+'",\
	    			"includeBroadband" : true,                           "includeIpVod" : true, "useLineup" : false, "offset" : "0",\
	    			"includePersonSearch" : true,                        "count" : "2", "includeBroadcast" : true, "includeFree" : true,\
	    			"includeVod" : true, "mergeOverridingCollections" : true, "minEndTime" : "2016-10-14 12:43:21", "mergeOverridingContent"\
	    			: true, "searchable" : true, "includeUnifiedItemType" : [ "channel" ], "orderBy" : [ "relevance", "strippedTitle" ],\
	    			"type" : "discovery1NumericUnifiedItemSearch"    }'
		response=requests.post(url=url,headers=headers,params=params,data=payload)
		assert re.search("channel",response.text)


	

	
    

       
		


