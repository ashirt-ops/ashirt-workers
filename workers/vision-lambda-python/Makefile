image_name = vision

.PHONY: clean
clean:
	rm -f requirements.txt

.PHONY: build
build: clean
	pipenv requirements > requirements.txt
	podman build -t $(image_name) .

.PHONY: run
run:
	podman run --rm --env-file ./.env -p 9000:8080 $(image_name)

.PHONY: start-msg
start-msg:
	@printf "\033[0;32mStarting Container...\033[0m\n"

.PHONY: start
start: build start-msg run

.PHONY: test-test
test-test:
	curl -XPOST "http://localhost:9000/2015-03-31/functions/function/invocations" -d '{"type": "test"}' | json_pp | pygmentize -l json

.PHONY: test-process-img
test-process-img:
	curl -XPOST "http://localhost:9000/2015-03-31/functions/function/invocations" -d '{"type": "evidence_created", "evidenceUuid": "d5bae379-a84a-4b4c-8796-5a708d0e3c47", "operationSlug": "asdgdfs", "contentType": "image"}' | json_pp | pygmentize -l json

.PHONY: test-unsupported
test-unsupported:
	curl -XPOST "http://localhost:9000/2015-03-31/functions/function/invocations" -d '{"type": "unsupported"}' | json_pp | pygmentize -l json
