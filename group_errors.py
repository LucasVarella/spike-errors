import csv
import json
from collections import OrderedDict

INPUT = "errors-extracted.csv"
OUTPUT = "errors-unique.json"
GROUP_KEYS = ("kind", "provider", "model", "raw_error", "step_type")

groups = {}

with open(INPUT, newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        key = tuple(row[k] for k in GROUP_KEYS)
        if key not in groups:
            groups[key] = {
                "count": 0,
                "kind": row["kind"],
                "provider": row["provider"],
                "model": row["model"],
                "message": row.get("message", ""),
                "raw_error": row["raw_error"],
                "step_type": row["step_type"],
                "suggested_action": None,
                "details": None,
                "metrics": None,
            }
        g = groups[key]
        g["count"] += 1

        if g["suggested_action"] is None and row.get("suggested_action", "").strip():
            g["suggested_action"] = row["suggested_action"]

        if g["details"] is None and row.get("details", "").strip():
            try:
                g["details"] = json.loads(row["details"])
            except json.JSONDecodeError:
                g["details"] = row["details"]

        if g["metrics"] is None and row.get("metrics", "").strip():
            try:
                g["metrics"] = json.loads(row["metrics"])
            except json.JSONDecodeError:
                g["metrics"] = row["metrics"]

result = sorted(groups.values(), key=lambda g: g["count"], reverse=True)

with open(OUTPUT, "w", encoding="utf-8") as f:
    json.dump(result, f, indent=2, ensure_ascii=False)

# Verification
total = sum(g["count"] for g in result)
print(f"Groups: {len(result)}")
print(f"Total rows: {total}")
print(f"\nTop 5:")
for g in result[:5]:
    print(f"  [{g['count']:3d}] {g['kind']} | {g['provider']} | {g['model']} | {g['step_type']}")
    raw = g["raw_error"]
    print(f"        {raw[:100]}{'...' if len(raw) > 100 else ''}")
