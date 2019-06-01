from docker.tivo.com/synthetic-tests-pytest:stable

# Pre-requisite for confluent-kafka-python==0.11.4
RUN apk add build-base librdkafka-dev

# Get the synthetic tests library using jfrog
ARG VERSION=1.0.0
RUN curl -o /app/synthetic-tests-library-apis-$VERSION.tar.gz http://repo-vip.tivo.com:8081/artifactory/bs35-storage/synthetic-tests-library-apis/1.0.0/synthetic-tests-library-apis-$VERSION.tar.gz
RUN pip install --upgrade  /app/synthetic-tests-library-apis-$VERSION.tar.gz


# Get the confluent-kafka-python-wrapper library
RUN curl -o /app/confluent_kafka_wrapper_library-$VERSION.tar.gz http://repo-vip.tivo.com:8081/artifactory/bs35-storage/confluent_kafka_wrapper_library/1.0.0/confluent_kafka_wrapper_library-$VERSION.tar.gz
# Install confluent-kafka-python-wrapper library
RUN pip install --upgrade /app/confluent_kafka_wrapper_library-$VERSION.tar.gz


RUN pip install xmltodict
ADD tests/body-update-service /app/tests/body-update-service
