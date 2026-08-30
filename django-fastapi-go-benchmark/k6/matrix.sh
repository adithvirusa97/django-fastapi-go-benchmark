#!/bin/sh
set -eu
for vus in 1 50 100 200; do
  for target in django fastapi golang fastapi-granian; do
  # for target in fastapi-granian; do
    echo "=== $target / $vus VUs ==="
    docker compose --profile benchmark run --rm -e TARGET="$target" -e VUS="$vus" -e DURATION="30s" k6 run /scripts/benchmark.js
  done
done
docker compose --profile benchmark run --rm analyzer
