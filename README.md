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


## Prometheus/Grafana

Prometheus scrapes `/metrics` from all three applications. Grafana is pre-provisioned with Prometheus as its data source.

Note: the application metric sets are intentionally minimal in this starter. For a production-quality observability comparison, add the same HTTP request counters/histograms to all three applications with identical metric names and labels.


