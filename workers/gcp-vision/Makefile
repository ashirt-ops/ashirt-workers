imageNameDev = gcp-vision-dev
imageName = gcp-vision

.PHONY: build_dev
build_dev:
	docker build -t $(imageNameDev) -f Dockerfile.dev .

.PHONY: build_release
build_release:
	docker build -t $(imageName) -f Dockerfile.prod .

run_dev:
	docker compose up --build
