## Makefile
up:
	docker-compose up

build:
	docker-compose build

down:
	docker-compose down

lint:
	docker-compose run --rm app black .
