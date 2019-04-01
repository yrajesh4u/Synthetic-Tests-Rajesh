from pytest_lib import config
from datetime import datetime
import json


common_payload =  {
    "includePaid" : "true",
    "numRelevantItems" : "100",
    "includeBroadband" : "true",
    "includeIpVod" : "true",
    "useLineup" : "false",
    "offset" : "0",
    "includePersonSearch" : "true",
    "includeBroadcast" : "true",
    "includeFree" : "true",
    "includeVod" : "true",
    "mergeOverridingCollections" : "true",
    "minEndTime" : str(datetime.now()),
    "mergeOverridingContent" : "true",
    "searchable" : "true",
    "orderBy" : [
        "relevance",
        "strippedTitle"
    ],
    "type" : "discovery1NumericUnifiedItemSearch"
}
class Testtextserachpayload:
    
    """
    
    returns url,params, and payload

    """

    """

    URL SECTION

    """
                               
    @staticmethod
    def generate_textsearch_url(device_domain_config=None):
    
        return 'http://'+ config['MiddlemindVip'] + ':' + config['mm_port'] + '/' + device_domain_config ["mind_version"]

    

    """

    PARAM SECTION

    """

    @staticmethod
    def textsearch_params(device_domain_config=None):
        return  {"type":"discovery1NumericUnifiedItemSearch","bodyId": device_domain_config["bodyId"]}


    """

    PAYLOAD SECTION

    """


    @staticmethod
    def textsearch_collection_payload(device_domain_config=None):
        combined_payload=json.dumps({**common_payload,**device_domain_config["payload_collection"]})
        return combined_payload

    @staticmethod
    def textsearch_content_payload(device_domain_config=None):
        combined_payload=json.dumps({**common_payload,**device_domain_config["payload_content"]})
        return combined_payload

    @staticmethod
    def textsearch_person_payload(device_domain_config=None):
        combined_payload=json.dumps({**common_payload,**device_domain_config["payload_person"]})
        return combined_payload

    @staticmethod
    def textsearch_team_payload(device_domain_config=None):
        combined_payload=json.dumps({**common_payload,**device_domain_config["payload_team"]})
        return combined_payload

    @staticmethod
    def textsearch_channel_payload(device_domain_config=None):
        combined_payload=json.dumps({**common_payload,**device_domain_config["payload_channel"]})
        return combined_payload
        