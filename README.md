# Django vs FastAPI vs Go — Reproducible Backend Benchmark

This project benchmarks equivalent HTTP + PostgreSQL workloads across Django, FastAPI and Go, with Docker, k6, Prometheus, Grafana and automated charts.

## Architecture

Client/load generator → Django / FastAPI / Go → PostgreSQL
                              ↓
                         Prometheus → Grafana

## Services

- Django: http://localhost:8003
- FastAPI: http://localhost:8001
- Go: http://localhost:8002
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3000 (admin/admin)

## Start everything

```bash
docker compose up -d --build
```

Check:

```bash
curl http://localhost:8003/health
curl http://localhost:8001/health
curl http://localhost:8002/health
```

## Run benchmark

The default test is 50 virtual users for 30 seconds against `GET /users/5000`.

```bash
make benchmark
```

Custom load:

```bash
VUS=200 DURATION=60s make benchmark
```

Results are written to `results/`:

- `django.json`
- `fastapi.json`
- `golang.json`
- `summary.csv`
- `charts/*.png`

## Important methodology

Do not publish the first numbers as universal framework limits. Repeat each test several times, warm the services first, keep CPU/RAM limits identical, keep PostgreSQL identical, and benchmark one target at a time. Record the exact Docker, OS, CPU, RAM, versions, worker counts, VUs and test duration with every result.

For a stronger study, add separate scenarios for:

1. `/health` — framework/server overhead, no database.
2. `/users/{id}` — PostgreSQL I/O + JSON serialization.
3. CPU-heavy endpoint — application computation.
4. POST endpoint — validation + database write.
5. Mixed workload — realistic traffic distribution.

## Prometheus/Grafana

Prometheus scrapes `/metrics` from all three applications. Grafana is pre-provisioned with Prometheus as its data source.

Note: the application metric sets are intentionally minimal in this starter. For a production-quality observability comparison, add the same HTTP request counters/histograms to all three applications with identical metric names and labels.


