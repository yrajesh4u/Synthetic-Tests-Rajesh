from docker.tivo.com/synthetic-tests-pytest:stable

# Set the working directory
WORKDIR /app
	
# Get the synthetic tests library
ARG VERSION=1.0.0
RUN curl -o /app/synthetic-tests-library-apis-$VERSION.tar.gz http://repo-vip.tivo.com:8081/artifactory/bs35-storage/synthetic-tests-library-apis/1.0.0/synthetic-tests-library-apis-$VERSION.tar.gz
	
# Install the synth_test_lib
RUN pip install --upgrade /app/synthetic-tests-library-apis-$VERSION.tar.gz

# Add the tests to /app
ADD tests/textsearchbynumbers /app/tests/textsearchbynumbers
