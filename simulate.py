#!/usr/bin/env python3
"""Estimate operational risk for SQL schema migrations."""
import argparse
import json
import re
from pathlib import Path


def analyze(sql, table_rows=None):
    table_rows = table_rows or {}
    normalized = " ".join(sql.lower().split())
    risks = []
    if re.search(r"\bdrop\s+(table|column)\b", normalized):
        risks.append({"kind": "irreversible-ddl", "severity": "high"})
    if re.search(r"\balter\s+table\b.*\b(add|alter|drop)\b", normalized):
        risks.append({"kind": "table-lock-risk", "severity": "medium"})
    tables = re.findall(r"\b(?:update|alter table)\s+([\w.]+)", normalized)
    estimates = []
    for table in tables:
        rows = table_rows.get(table, 0)
        if rows:
            estimates.append({"table": table, "rows": rows, "estimated_seconds": round(rows / 50000, 2)})
            if rows >= 1_000_000:
                risks.append({"kind": "large-backfill", "severity": "high", "table": table})
    return {"risks": risks, "estimates": estimates, "safe": not any(r["severity"] == "high" for r in risks)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("migration"); parser.add_argument("--stats")
    args = parser.parse_args()
    stats = json.loads(Path(args.stats).read_text()) if args.stats else {}
    report = analyze(Path(args.migration).read_text(), stats)
    print(json.dumps(report, indent=2))
    raise SystemExit(0 if report["safe"] else 1)


if __name__ == "__main__":
    main()
