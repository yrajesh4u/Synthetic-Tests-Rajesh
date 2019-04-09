from docker.tivo.com/synthetic-tests-pytest:stable

# Get the synthetic tests library using jfrog
ARG VERSION=1.0.0
RUN curl -o /app/synthetic-tests-library-apis-$VERSION.tar.gz http://repo-vip.tivo.com:8081/artifactory/bs35-storage/synthetic-tests-library-apis/1.0.0/synthetic-tests-library-apis-$VERSION.tar.gz
RUN pip install --upgrade  /app/synthetic-tests-library-apis-$VERSION.tar.gz

RUN pip install xmltodict
ADD tests/body_update_service /app/tests/body_update_service
