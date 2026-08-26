#!/bin/sh
set -eu
for vus in 1 10 30 50 100 200; do
  for target in django fastapi golang; do
    echo "=== $target / $vus VUs ==="
    docker compose --profile benchmark run --rm -e TARGET="$target" -e VUS="$vus" -e DURATION="30s" k6 run /scripts/benchmark.js
  done
done
docker compose --profile benchmark run --rm analyzer
