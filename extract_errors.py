import csv
import json

INPUT = "/home/nak/Projects/flambra/spike-erros/errors-since-2026-01-01.csv"
OUTPUT = "/home/nak/Projects/flambra/spike-erros/errors-extracted.csv"

SIMPLE_FIELDS = [
    "kind", "model", "message", "step_id", "provider", "billable?",
    "raw_error", "step_type", "workflow_id", "retry_policy",
    "prediction_id", "webhook_run_id", "workflow_run_id", "suggested_action",
]
COMPLEX_FIELDS = ["metrics", "inputs", "output", "details"]
ALL_FIELDS = SIMPLE_FIELDS + COMPLEX_FIELDS

with open(INPUT, newline="") as fin, open(OUTPUT, "w", newline="") as fout:
    reader = csv.DictReader(fin)
    writer = csv.DictWriter(fout, fieldnames=ALL_FIELDS)
    writer.writeheader()

    count = 0
    for row in reader:
        raw = row.get("error", "").strip()
        if not raw:
            continue
        error = json.loads(raw)
        out = {}
        for f in SIMPLE_FIELDS:
            out[f] = error.get(f, "")
        for f in COMPLEX_FIELDS:
            val = error.get(f)
            out[f] = json.dumps(val) if val is not None else ""
        writer.writerow(out)
        count += 1

print(f"Wrote {count} rows to {OUTPUT}")
