.PHONY: up down logs benchmark benchmark-django benchmark-fastapi benchmark-golang analyze

up:
	docker compose up -d --build

down:
	docker compose down

logs:
	docker compose logs -f

benchmark: benchmark-django benchmark-fastapi benchmark-golang analyze

benchmark-django:
	docker compose --profile benchmark run --rm \
		-e TARGET=django \
		-e VUS=$${VUS:-50} \
		-e DURATION=$${DURATION:-30s} \
		k6 run /scripts/benchmark.js

benchmark-fastapi:
	docker compose --profile benchmark run --rm \
		-e TARGET=fastapi \
		-e VUS=$${VUS:-50} \
		-e DURATION=$${DURATION:-30s} \
		k6 run /scripts/benchmark.js

benchmark-golang:
	docker compose --profile benchmark run --rm \
		-e TARGET=golang \
		-e VUS=$${VUS:-50} \
		-e DURATION=$${DURATION:-30s} \
		k6 run /scripts/benchmark.js

analyze:
	docker compose --profile benchmark run --rm analyzer