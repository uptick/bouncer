REPO ?= 305686791668.dkr.ecr.ap-southeast-2.amazonaws.com
TAG ?= latest
IMAGE ?= ${REPO}/bouncer:${TAG}

release:
	docker login -u AWS -p $(shell aws ecr get-login-password --region ap-southeast-2) https://${REPO} &&  docker push  ${IMAGE}

build:
	docker build -t ${IMAGE} .

run:
	docker run -e GUNICORN_CMD_ARGS="--reload"  -v $(shell pwd)/app:/app -p 90:80 --rm -it ${IMAGE}



