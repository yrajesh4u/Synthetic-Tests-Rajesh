from docker.tivo.com/synthetic-tests-pytest:stable

RUN pip install xmltodict
ADD tests/body_update_service /app/tests/body_update_service
