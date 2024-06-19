imageNameDev = vision-web-dev
imageName = vision-web

.PHONY: build_dev
build_dev:
	podman build -t $(imageNameDev) -f Dockerfile.dev .

.PHONY: build_release
build_release:
	podman build -t $(imageName) -f Dockerfile.prod .

run_dev:
	podman compose up --build

.PHONY: test-test
test-test:
	curl -XPOST "http://localhost:9000/test" -d '{"type": "test"}' 

.PHONY: test-process-img
test-process-img:
	curl -XPOST "http://localhost:9000/process" \
	-H "Content-Type: application/json" \
	-d '{"type": "evidence_created", "evidenceUuid": "seed_dursleys", "operationSlug": "HPSS", "contentType": "image"}'

.PHONY: test-unsupported
test-unsupported:
	curl -XPOST "http://localhost:9000/process" \
	-H "Content-Type: application/json" \
	-d '{"type": "unsupported"}'
