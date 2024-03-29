import requests
import time
import json
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

    def api_call(self, url, method, data=None, headers=None, timeout=API_TIMEOUT,
                 cert=None, verify=None, status_code=200):
        response = None
        if type(headers) == dict:
            headers = {**self.HEADERS, **headers}
        try:
            if method.upper() == 'POST':
                response = requests.post(url, data=data, headers=headers, timeout=timeout, cert=cert, verify=verify)
            elif method.upper() == 'GET':
                response = requests.get(url=url, timeout=timeout)
        except ConnectionError as e:
            print("ERROR in %s call: %s " % (str(method).upper(), e))
        synthassert(
            response.status_code == status_code,
            message="Expected: {}, Actual: {}".format(status_code, response.status_code),
            response=response
        )
        return response

    @staticmethod
    def get_kafka_key_value_messages(consumer, timeout=40):
        end_time = time.time() + timeout
        data = []
        while time.time() < end_time:
            message = consumer.get_latest_message_along_with_key(timeout=20)

            if message:
                data.append(message)
        return data

    def prov_device_activate_kafka_validation(self, consumer, transaction_id, timeout=120):
        end_time = time.time() + timeout
        while time.time() < end_time:
            data = self.get_kafka_key_value_messages(consumer=consumer)

            for msg in data:
                    msg_str = [*msg.values()][0].split('\n')[-1]
                    if 'transactionId' in msg_str:
                        value = json.loads(msg_str)
                        if value['transactionId'] == transaction_id:
                            return True, value['serviceFeAccountId']

        return False, 'Not able to find serviceFeAccountId for given transactionId=%s' % transaction_id

    def tve_service_activate_kafka_validation(self, consumer, request_id, timeout=120):
        end_time = time.time() + timeout
        while time.time() < end_time:
            data = self.get_kafka_key_value_messages(consumer=consumer)

            for msg in data:
                msg_str = [*msg.values()][0].split('\n')[-1]
                if 'transactionId' in msg_str:
                    value = json.loads(msg_str)
                    if value['transactionId'] == request_id:
                        return True, value['tivoCustomerId']

        return False, 'Not able to find tivoCustomerId for given request_id=%s' % request_id

    def prov_device_cancle_kafka_validation(self, consumer, service_fe_account_id, timeout=120):
        end_time = time.time() + timeout
        while time.time() < end_time:
            data = self.get_kafka_key_value_messages(consumer=consumer)

            for msg in data:
                    msg_str = [*msg.values()][0].split('\n')[-1]
                    if 'serviceFeAccountId' in msg_str:
                        value = json.loads(msg_str)
                        if (value['serviceFeAccountId'] == service_fe_account_id) and \
                                ('pr1ProvDeviceCancel' in value['transactionId']) and value['serviceState'] == 'cancel':
                            return True

        return False

    def tve_service_cancel_kafka_validation(self, consumer, tivo_customer_id, request_id, timeout=120):
        end_time = time.time() + timeout
        while time.time() < end_time:
            data = self.get_kafka_key_value_messages(consumer=consumer)

            for msg in data:
                msg_str = [*msg.values()][0].split('\n')[-1]
                if 'tivoCustomerId' in msg_str:
                    value = json.loads(msg_str)
                    if value['tivoCustomerId'] == tivo_customer_id and ('bodyId' not in value) and \
                            (value['transactionId'] != request_id):
                        return True

        return False
