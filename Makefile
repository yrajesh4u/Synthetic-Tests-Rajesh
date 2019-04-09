all: build

SUITE := textsearchbynumbers
SUB := $(or ${SUB},${SUB},'')
TAG := $(or ${TAG},${TAG},latest)
IMAGE=docker.tivo.com/synthetic-tests-$(SUITE)

ifeq ($(SUB), '')
	REPO_IMAGE=docker.tivo.com/synthetic-tests-$(SUITE)
else
	REPO_IMAGE=docker.tivo.com/$(SUB)/synthetic-tests-$(SUITE)
endif

build:
	docker login docker.tivo.com
	docker build $(CACHE) $(PULL) -t $(IMAGE) .

test:
	docker run --rm $(IMAGE) --suite $(SUITE) --probe test --target production --action test --debug true

run:
	docker run --rm $(IMAGE) --suite $(SUITE) --probe $(PROBE) --target $(TARGET) --debug true

print_config:
	docker run --rm $(IMAGE) --suite $(SUITE) --probe $(PROBE) --target $(TARGET) --action print_config --debug true

deploy: build
	docker tag $(IMAGE) $(REPO_IMAGE):$(TAG)
	docker push $(REPO_IMAGE):$(TAG)

pull:
	$(eval PULL := --pull )

nocache:
	$(eval CACHE := --no-cache )