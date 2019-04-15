import requests
from synth_test_lib.synthassert import synthassert

class BodyUpdateService:
    API_TIMEOUT = 700
    HEADERS = {}
    HEADERS.setdefault('Accept-Language', 'en')
    HEADERS.setdefault('User-Agent', 'Automation-QA')
    HEADERS.setdefault('Content-Type', 'text/xml')
    HEADERS.setdefault('Accept-Encoding', 'gzip,deflate')
    HEADERS.setdefault('SchemaVersion', '2')
    HEADERS.setdefault('Accept', 'application/json')
    HEADERS.setdefault('ApplicationName', 'bodyUpdateServiceSyntheticTests')

    def api_call(self, url, method, data=None, headers=None, timeout=API_TIMEOUT, cert=None, verify=None, status_code=200):
        response = None
        if type(headers) == dict:
            headers = {**self.HEADERS, **headers}
        try:
            if method.upper() == 'POST':
                response = requests.post(url, data=data, headers=headers, timeout=timeout, cert=cert, verify=verify)
            elif method.upper() == 'GET':
                response = requests.get(url, headers=headers, timeout=timeout)
        except ConnectionError as e:
            print("ERROR in %s call: %s " % (str(method).upper(), e))

        synthassert(
            response.status_code == status_code,
            message="Expected: {}, Actual: {}".format(status_code, response.status_code),
            response=response
        )

        return response
