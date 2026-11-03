#!/usr/bin/env python3
"""Validate independent *synthetic* service desk and IT operations lab datasets.

This never connects to corporate systems, executes administrative PowerShell,
or asserts that unrelated project datasets reconcile.
"""
from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HELPDESK = ROOT / "enterprise-helpdesk-support-lab"
OPS = ROOT / "enterprise-it-operations-lab"

TICKETS = HELPDESK / "tickets/ticket-register.csv"
USERS = HELPDESK / "datasets/users.csv"
MONTHLY = OPS / "dashboards/datasets/monthly-kpis.csv"

TICKET_COLUMNS = {"ticket_id", "created_at", "resolved_at", "priority",
                  "category", "title", "requester", "technician",
                  "sla_result", "resolution_minutes", "root_cause", "status"}
USER_COLUMNS = {"user_id", "display_name"}
MONTHLY_COLUMNS = {"Month", "Tickets", "SLA", "AvgResolution", "FCR", "CSAT",
                   "PatchCompliance", "BackupSuccess", "ChangeSuccess",
                   "MTTR", "CloudCost"}
PCT = {"SLA", "FCR", "PatchCompliance", "BackupSuccess", "ChangeSuccess"}


def read_csv(path: Path, required: set[str]) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as stream:
        reader = csv.DictReader(stream, strict=True)
        headers = reader.fieldnames or []
        if len(headers) != len(set(headers)) or not required.issubset(headers):
            raise ValueError(f"{path.name}: missing/duplicate required CSV column")
        records = list(reader)
    if not records:
        raise ValueError(f"{path.name}: empty dataset")
    for i, row in enumerate(records, 2):
        if None in row or any(v is None for v in row.values()):
            raise ValueError(f"{path.name} row {i}: surplus or missing CSV cells")
        if any(not str(row.get(key, "")).strip() for key in required):
            raise ValueError(f"{path.name} row {i}: blank required value")
    return records


def metrics(tickets: list[dict[str, str]], users: list[dict[str, str]],
            months: list[dict[str, str]]) -> dict:
    if not tickets or not users or not months:
        raise ValueError("empty ticket, user, or monthly KPI series")
    user_ids = [r["user_id"] for r in users]
    if len(set(user_ids)) != len(user_ids):
        raise ValueError("Duplicate user IDs")
    known_users = set(user_ids)
    ticket_ids = set()
    priorities = Counter()
    categories = Counter()
    sla = Counter()
    durations = []
    for row in tickets:
        ticket_id = row["ticket_id"]
        if ticket_id in ticket_ids:
            raise ValueError(f"Duplicate ticket ID {ticket_id}")
        ticket_ids.add(ticket_id)
        if row["requester"] not in known_users:
            raise ValueError(f"{ticket_id}: unknown requester")
        if row["priority"] not in {"P1", "P2", "P3", "P4"}:
            raise ValueError(f"{ticket_id}: invalid priority")
        if row["sla_result"] not in {"Met", "Breached"}:
            raise ValueError(f"{ticket_id}: invalid SLA status")
        if row["status"] not in {"Resolved", "Closed"}:
            raise ValueError(f"{ticket_id}: no confirmed resolved timestamp status")
        try:
            created = datetime.fromisoformat(row["created_at"])
            resolved = datetime.fromisoformat(row["resolved_at"])
            recorded_minutes = int(row["resolution_minutes"])
        except (ValueError, TypeError) as exc:
            raise ValueError(f"{ticket_id}: invalid date or duration") from exc
        if created.tzinfo != resolved.tzinfo:
            raise ValueError(f"{ticket_id}: inconsistent timezones")
        measured_minutes = (resolved - created).total_seconds() / 60
        if recorded_minutes < 0 or abs(measured_minutes - recorded_minutes) > 0.01:
            raise ValueError(f"{ticket_id}: resolution minutes disagree with timestamps")
        durations.append(recorded_minutes)
        priorities[row["priority"]] += 1
        categories[row["category"]] += 1
        sla[row["sla_result"]] += 1
    checked_months = set()
    clean_months = []
    for row in months:
        month = row["Month"]
        try:
            parsed_month = datetime.strptime(month, "%Y-%m")
            if parsed_month.strftime("%Y-%m") != month:
                raise ValueError(f"Invalid KPI month: {month}")
        except ValueError as exc:
            raise ValueError(f"Invalid KPI month: {month}") from exc
        if month in checked_months:
            raise ValueError(f"Duplicate KPI month {month}")
        checked_months.add(month)
        m = {"month": month}
        for key in MONTHLY_COLUMNS - {"Month"}:
            try:
                number = float(row[key])
            except (ValueError, TypeError) as exc:
                raise ValueError(f"{month}: invalid {key}") from exc
            if not (0 <= number < float("inf")):
                raise ValueError(f"{month}: out-of-range {key}")
            if key in PCT and number > 100:
                raise ValueError(f"{month}: percentage outside 0-100 ({key})")
            if key == "CSAT" and number > 5:
                raise ValueError(f"{month}: CSAT outside 0-5")
            if key == "Tickets" and not number.is_integer():
                raise ValueError(f"{month}: noninteger tickets")
            m[key] = int(number) if key == "Tickets" else number
        clean_months.append(m)
    clean_months.sort(key=lambda row: row["month"])
    return {
        "scope": "Synthetic helpdesk tickets and independent synthetic IT operations KPI snapshots",
        "data_comparability": "Do not reconcile helpdesk ticket counts to independent IT Operations monthly KPI series",
        "ticket_count": len(tickets),
        "user_count": len(users),
        "resolved_ticket_count": len(durations),
        "sla_met_count": sla["Met"],
        "sla_breached_count": sla["Breached"],
        "average_resolution_minutes": round(sum(durations) / len(durations), 2),
        "priority_counts": dict(sorted(priorities.items())),
        "category_counts": dict(sorted(categories.items())),
        "monthly_kpis": clean_months,
        "dataset_status": "SOURCE_CONSISTENT_SYNTHETIC",
        "not_verified": ["Live ITSM data", "Real ticket SLA outcomes",
                         "Live PowerShell / AD / M365 execution",
                         "Production security, incident or deployment efficacy"],
    }


def validate() -> dict:
    return metrics(read_csv(TICKETS, TICKET_COLUMNS),
                   read_csv(USERS, USER_COLUMNS),
                   read_csv(MONTHLY, MONTHLY_COLUMNS))


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--output", type=Path, default=ROOT / "reports/itops-source-validation.json")
    args = ap.parse_args()
    result = validate()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: v for k, v in result.items() if k != "monthly_kpis"}, indent=2))


if __name__ == "__main__":
    main()
