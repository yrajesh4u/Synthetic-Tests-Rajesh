import pytest
from pytest_lib import config
from kafka_lib.confluent_kafka_msg_consumer import KafkaMsgConsumer


@pytest.fixture(scope="class", autouse=True)
def prov_device_activate_kafka_consumer(request):
	conf = {
		'enable.auto.commit': True,
		'log.connection.close': False,
		'default.topic.config': {
			'auto.offset.reset': 'latest'
		}
	}
	consumer = KafkaMsgConsumer(
		kafka_host_name=config["kafka_host"],
		topic_name=config["feExtDeviceTopic"],
		group_id="Test-Consumer-Group-01"
	)
	consumer.start_consumer(conf)
	request.addfinalizer(consumer.stop_consumer)
	return consumer

@pytest.fixture(scope="class", autouse=True)
def tve_service_activate_kafka_consumer(request):
	conf = {
		'enable.auto.commit': True,
		'log.connection.close': False,
		'default.topic.config': {
			'auto.offset.reset': 'latest'
		}
	}
	consumer = KafkaMsgConsumer(
		kafka_host_name=config["kafka_host"],
		topic_name=config["tcidToTsnMap"],
		group_id="Test-Consumer-Group-02"
	)
	consumer.start_consumer(conf)
	request.addfinalizer(consumer.stop_consumer)
	return consumer

