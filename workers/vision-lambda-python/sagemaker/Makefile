image_name = vision

.PHONY: clean
clean:
	rm -f requirements.txt

.PHONY: build
build: clean
	pipenv requirements > requirements.txt
	docker build -t $(image_name) .

.PHONY: run
run:
	docker run --rm -p 9000:8080 $(image_name)

.PHONY: start-msg
start-msg:
	@printf "\033[0;32mStarting Container...\033[0m\n"

.PHONY: start
start: build start-msg run

.PHONY: test-invoke
test-invoke:
	curl -XPOST localhost:9000/invocations -d '{"input":"hello!"}' -H 'Content-Type: application/json'

.PHONY: test-ping
test-ping:
	curl localhost:9000/ping
