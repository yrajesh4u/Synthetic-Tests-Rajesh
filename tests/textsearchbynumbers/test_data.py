from pytest_lib import config
from datetime import datetime
import json

  
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
    def textsearch_payload(device_domain_config=None):
        payload={
                    "bodyId": device_domain_config["bodyId"],
                    "count": 16,
                    "deviceType": [
                                    "stb"
                                ],
                    "includeBroadband": "true",
                    "includeBroadcast": "true",
                    "includeIpVod": "true",
                    "includeUnifiedItemType": [
                                                    "collection",
                                                    "content",
                                                    "person",
                                                    "channel",
                                                    "team"
                                            ],
                    "levelOfDetail": "medium",
                    "mergeOverridingCollections": "true",
                    "mergeOverridingContent": "true",
                    "minEndTime": str(datetime.now()),
                    "numRelevantItems": 50,
                    "numbers": "3743637*",
                    "offset": 0,
                    "orderBy": [
                                    "relevance",
                                    "strippedTitle"
                                ],
                    "searchable": "true",
                    "useLineup": "false",
                    "type": "discovery1NumericUnifiedItemSearch"
                    }
        return json.dumps(payload)

    