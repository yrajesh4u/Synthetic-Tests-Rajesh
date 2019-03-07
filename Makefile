all: build
 
 
SUITE := test_textsearchbynumbers
IMAGE=docker.tivo.com/synthetic-tests-$(SUITE)
TAG := $(or ${TAG},${TAG},latest)
 
build:
	docker login docker.tivo.com
	docker build -t $(IMAGE) .
 
run:
	docker run --rm --network=host -it $(IMAGE) --suite $(SUITE) --probe $(PROBE) --target $(TARGET) --debug true
 
print_config:
    docker run --rm --network=host -it $(IMAGE) --suite $(SUITE) --probe $(PROBE) --target $(TARGET) --action print_config --debug true
 
deploy: build
    docker tag $(IMAGE) $(IMAGE):$(TAG)
    docker push $(IMAGE):$(TAG)
