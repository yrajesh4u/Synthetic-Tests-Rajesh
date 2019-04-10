from pytest_lib import config


class TestDataEnvelopes:
    npvr_bodyId = None
    internalId = None
    bodyId = None

    def data_ProvAccountStore(self):
        url = 'http://%s/pr1ProvAccountStore' % config['deviceActivate']
        method = 'POST'
        data = '''{"accountAlaCartePackage": ["NpvrMediumPackage"],
                    "feOperatorName": "CableCo",
                    "partnerCustomerId":  "''' + config['random_number'] + '''",
                    "type": "pr1ProvAccountStore"}'''
        return url, method, data

    def data_ProvDeviceActivate(self):
        url = 'http://%s/pr1ProvDeviceActivate' % config['deviceActivate']
        method = 'POST'
        data = '''{"accountAlaCartePackage": ["NpvrMediumPackage"],
                "deviceAlaCarteFeatureAttributeValue": [
                {
                    "attributeName": "npvrAllowRecording-allowNpvrRecording",
                    "attributeValue": "true",
                    "type": "provFeatureAttributeValue"
                }
                ],
                "deviceAlaCartePackage": ["CableCo-Device-TIVOCO2"],
                "deviceType": "npvr",
                "feOperatorName": "CableCo",
                "partnerCustomerId": "''' + config['random_number'] + '''",
                "type": "pr1ProvDeviceActivate"}'''
        return url, method, data

    def data_anonymizerPartnerExternalIdTranslate(self):
        url = 'http://%s/anonymizerPartnerExternalIdTranslate?type=anonymizerPartnerExternalIdTranslate' % \
              config['anonymizer']
        method = 'POST'
        data = '''{"partnerExternalId": "''' + config['random_number'] + '''",
                "idType": "''' + config['idType'] + '''",
                "partnerId":"tivo:pt.3689",
                "type":"anonymizerPartnerExternalIdTranslate"}'''
        return url, method, data

    def data_npvrEnablementSearch(self):
        url = 'http://%s/tacomind/v13/do?type=npvrEnablementSearch&ApplicationName=bodyUpdateServiceSyntheticTests' % \
              config['npvrEnablement']
        method = 'POST'
        data = '''{"accountId": "''' + self.internalId + '''",
                "type": "npvrEnablementSearch"}'''
        return url, method, data

    def data_tveServiceActivate(self):
        url = 'https://%s/itmind/mind14?type=tveServiceActivate' % config['serviceActivate']
        method = 'POST'
        data = '''<tveServiceActivate>
                <contract>
                <customer>
                <partnerCustomerId>''' + config['random_number'] + '''</partnerCustomerId>
                </customer>
                <device>
                <deviceType>iPad</deviceType>
                <msoServiceId>TIVOCO1</msoServiceId>
                </device>
                </contract>
                </tveServiceActivate>'''
        return url, method, data

    def data_bodyConfigSearch(self):
        url = 'http://%s/mind/mind21?type=bodyConfigSearch&bodyId=tsn:%s' % (config['bodyConfig'], self.bodyId)
        method = 'POST'
        data = '''{"bodyId": "tsn:''' + self.bodyId + '''",
                  "levelOfDetail": "high",
                  "noLimit": "true",
                  "type": "bodyConfigSearch"}'''
        return url, method, data

    def data_pr1ProvDeviceCancel(self):
        url = 'http://%s/pr1ProvDeviceCancel' % config['deviceActivate']
        method = 'POST'
        data = '''{"bodyId": "''' + self.npvr_bodyId + '''",
                  "feOperatorName": "CableCo",
                  "partnerCustomerId": "''' + config['random_number'] + '''",
                  "type": "pr1ProvDeviceCancel"}'''
        return url, method, data

    def data_tveServiceCancel(self):
        url = 'https://%s/itmind/mind14?type=tveServiceCancel' % config['serviceActivate']
        method = 'POST'
        data = '''<tveServiceCancel>
                    <cancellationCode>MS</cancellationCode>
                        <contract>
                        <customer>
                          <partnerCustomerId>''' + config['random_number'] + '''</partnerCustomerId>
                        </customer>
                    <device>
                    <tivoSerialNumber>''' + self.bodyId + '''</tivoSerialNumber>
                    </device>
                    </contract>
                    </tveServiceCancel>'''
        return url, method, data