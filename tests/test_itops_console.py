"""Source and negative-case tests for the synthetic Enterprise IT Operations labs."""
from __future__ import annotations

import copy
import json
import re
import tempfile
import unittest
from html.parser import HTMLParser
from pathlib import Path

from tools.validate_itops import (ROOT, MONTHLY, TICKETS, USERS,
    TICKET_COLUMNS, USER_COLUMNS, MONTHLY_COLUMNS,
    read_csv, metrics, validate)

HTML = ROOT / "demo/it-operations-console.html"


class SourceValidationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.users = read_csv(USERS, USER_COLUMNS)
        cls.tickets = read_csv(TICKETS, TICKET_COLUMNS)
        cls.months = read_csv(MONTHLY, MONTHLY_COLUMNS)

    def test_source_baseline_is_reproducible(self):
        report = validate()
        self.assertEqual((report["ticket_count"], report["user_count"],
                          len(report["monthly_kpis"])), (120, 250, 7))
        self.assertEqual(report["resolved_ticket_count"], 120)
        self.assertEqual(report["sla_met_count"], 120)
        self.assertEqual(report["sla_breached_count"], 0)
        self.assertEqual(sum(report["priority_counts"].values()),120)
        self.assertIn("Do not reconcile",report["data_comparability"])

    def test_duplicate_ticket_id_fails(self):
        rows=copy.deepcopy(self.tickets)
        rows[1]["ticket_id"]=rows[0]["ticket_id"]
        with self.assertRaisesRegex(ValueError,"Duplicate ticket ID"):
            metrics(rows,self.users,self.months)

    def test_duplicate_user_id_fails(self):
        rows=copy.deepcopy(self.users)
        rows[1]["user_id"]=rows[0]["user_id"]
        with self.assertRaisesRegex(ValueError,"Duplicate user IDs"):
            metrics(self.tickets,rows,self.months)

    def test_unknown_requester_fails(self):
        rows=copy.deepcopy(self.tickets)
        rows[0]["requester"]="User-NOT-FOUND"
        with self.assertRaisesRegex(ValueError,"unknown requester"):
            metrics(rows,self.users,self.months)

    def test_incorrect_resolution_time_fails(self):
        rows=copy.deepcopy(self.tickets)
        rows[0]["resolution_minutes"]="9999"
        with self.assertRaisesRegex(ValueError,"disagree"):
            metrics(rows,self.users,self.months)

    def test_reversed_resolution_timestamps_fail(self):
        rows=copy.deepcopy(self.tickets)
        rows[0]["resolved_at"]="2026-01-01T00:00"
        with self.assertRaisesRegex(ValueError,"disagree"):
            metrics(rows,self.users,self.months)

    def test_invalid_sla_status_fails(self):
        rows=copy.deepcopy(self.tickets)
        rows[0]["sla_result"]="Unknown"
        with self.assertRaisesRegex(ValueError,"invalid SLA"):
            metrics(rows,self.users,self.months)

    def test_invalid_priority_fails(self):
        rows=copy.deepcopy(self.tickets)
        rows[0]["priority"]="P99"
        with self.assertRaisesRegex(ValueError,"invalid priority"):
            metrics(rows,self.users,self.months)

    def test_duplicate_kpi_month_fails(self):
        rows=copy.deepcopy(self.months)
        rows.append(copy.deepcopy(rows[0]))
        with self.assertRaisesRegex(ValueError,"Duplicate KPI month"):
            metrics(self.tickets,self.users,rows)

    def test_out_of_range_sla_fails(self):
        rows=copy.deepcopy(self.months)
        rows[0]["SLA"]="101"
        with self.assertRaisesRegex(ValueError,"percentage outside"):
            metrics(self.tickets,self.users,rows)

    def test_out_of_range_csat_fails(self):
        rows=copy.deepcopy(self.months)
        rows[0]["CSAT"]="5.5"
        with self.assertRaisesRegex(ValueError,"CSAT outside"):
            metrics(self.tickets,self.users,rows)

    def test_duplicate_csv_header_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/"invalid.csv"
            p.write_text("a,a,other\n1,2,3\n")
            with self.assertRaisesRegex(ValueError,"duplicate"):
                read_csv(p,{"a","other"})

    def test_surplus_csv_data_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/"invalid.csv"
            p.write_text("a,b\n1,2,3\n")
            with self.assertRaisesRegex(ValueError,"surplus"):
                read_csv(p,{"a","b"})

    def test_missing_csv_required_field_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/"invalid.csv"
            p.write_text("a,b\n1,\n")
            with self.assertRaisesRegex(ValueError,"blank required"):
                read_csv(p,{"a","b"})


class ElementAudit(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids=set()
        self.labels=set()
        self.external_js=[]
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if "id" in a:
            if a["id"] in self.ids:
                raise AssertionError("duplicate element ID")
            self.ids.add(a["id"])
        if tag=="label" and "for" in a:
            self.labels.add(a["for"])
        if tag=="script" and "src" in a:
            self.external_js.append(a["src"])


class InteractiveConsoleTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.page=HTML.read_text(encoding="utf-8")
        match=re.search(r'<script id="itops-data" type="application/json">(.*?)</script>',cls.page,re.DOTALL)
        if not match:
            raise AssertionError("Offline source dataset missing")
        cls.data=json.loads(match.group(1))

    def test_embedded_source_ticket_records_are_exact(self):
        self.assertEqual(self.data["helpdesk_tickets"],read_csv(TICKETS,TICKET_COLUMNS))
        self.assertEqual(len(self.data["helpdesk_tickets"]),120)

    def test_embedded_monthly_series_is_exact(self):
        self.assertEqual(self.data["monthly_itops"],read_csv(MONTHLY,MONTHLY_COLUMNS))
        self.assertEqual(len(self.data["monthly_itops"]),7)

    def test_offline_accessible_controls(self):
        p=ElementAudit();p.feed(self.page)
        self.assertTrue({"search","priority","category","metric"}.issubset(p.ids))
        self.assertTrue({"search","priority","category","metric"}.issubset(p.labels))
        self.assertIn('aria-live="polite"',self.page)
        self.assertIn("textContent",self.page)
        self.assertIn("replaceChildren",self.page)
        self.assertNotIn("innerHTML",self.page)
        self.assertNotIn("fetch(",self.page)
        self.assertFalse(p.external_js)
        self.assertIn("no live ITSM",self.data["source"].lower())

    def test_ticket_data_is_not_falsely_joined_to_monthly_kpis(self):
        self.assertIn("must not be reconciled",self.page)
        self.assertNotEqual(120,sum(int(x["Tickets"]) for x in self.data["monthly_itops"]))
