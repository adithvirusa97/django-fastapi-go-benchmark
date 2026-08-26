import csv
import json
from pathlib import Path


RESULTS_DIR = Path("/results")
OUTPUT_FILE = RESULTS_DIR / "summary.csv"


def get_metric(metrics, metric_name, value_name, default="N/A"):
    metric = metrics.get(metric_name, {})
    values = metric.get("values", {})
    return values.get(value_name, default)


rows = []

for result_file in sorted(RESULTS_DIR.glob("*.json")):
    try:
        with result_file.open() as f:
            data = json.load(f)
    except (json.JSONDecodeError, OSError) as exc:
        print(f"Skipping {result_file}: {exc}")
        continue

    metrics = data.get("metrics", {})

    # framework = result_file.stem
    stem = result_file.stem
    framework, _, vus = stem.rpartition("_")
    if not framework:  # no underscore found, fall back
        framework, vus = stem, "unknown"

    rows.append(
        {
            "framework": framework,
            "vus": vus,
            "requests_per_second": get_metric(
                metrics,
                "http_reqs",
                "rate",
            ),
            "avg_latency_ms": get_metric(
                metrics,
                "http_req_duration",
                "avg",
            ),
            "p50_latency_ms": get_metric(
                metrics,
                "http_req_duration",
                "med",
            ),
            "p90_latency_ms": get_metric(
                metrics,
                "http_req_duration",
                "p(90)",
            ),
            "p95_latency_ms": get_metric(
                metrics,
                "http_req_duration",
                "p(95)",
            ),
            "p99_latency_ms": get_metric(
                metrics,
                "http_req_duration",
                "p(99)",
            ),
            "error_rate": get_metric(
                metrics,
                "http_req_failed",
                "rate",
            ),
        }
    )


with OUTPUT_FILE.open("w", newline="") as f:
    fieldnames = [
        "framework",
        "requests_per_second",
        "avg_latency_ms",
        "p50_latency_ms",
        "p90_latency_ms",
        "p95_latency_ms",
        "p99_latency_ms",
        "error_rate",
    ]

    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)


print(f"\nCreated: {OUTPUT_FILE}\n")

for row in rows:
    print(row)