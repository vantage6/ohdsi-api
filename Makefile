IMAGE = "harbor2.vantage6.ai/infrastructure/ohdsi-api"
TAG = "latest"
IMAGE_OPTS = "--progress=plain"


help:
	@echo "set-version   - set the version of all packages, needs VERSION"
	@echo "image         - build the docker image"
	@echo "push          - push the docker image to the registry"

set-version:
	echo $(VERSION) > VERSION;

image:
	docker build -t $(IMAGE):$(TAG) $(IMAGE_OPTS) .

push:
	docker push $(IMAGE):$(TAG)



