# IT operations validation and interactive console

## Quick review

Open [the offline interactive Service Operations Console](../demo/it-operations-console.html) in a browser, keeping the repository directory structure intact so the source references work.

The console shows **120 simulated Help Desk tickets** from `enterprise-helpdesk-support-lab/tickets/ticket-register.csv`, including recorded priorities, resolution durations, requesters, categories and synthetic SLA labels. The seven-month KPI visualization comes from a **separate** `enterprise-it-operations-lab/dashboards/datasets/monthly-kpis.csv` sample. The two independently authored datasets are **not** part of a single reconciled organization or observation period.

The Help Desk fixture currently marks all 120 cases resolved and SLA met. This is a property of authored sample data, **not a real operational SLA achievement claim**. The broader portfolio also documents a separately authorized read-only M365/Entra investigation; this demo does not ingest, summarize or alter that separate personal-tenant evidence.

## Reproduce offline checks

Python 3.11 or 3.12, using **only the Python standard library**:

```bash
python -m tools.validate_itops --output reports/itops-source-validation.json
python -m unittest discover -s tests -p 'test_*.py' -v
```

`tools/validate_itops.py` checks:

- Required and unique CSV headers, nonempty cells, duplicate IDs and requester-to-user references.
- Help Desk ticket status, priority, SLA labels, valid resolution timestamps and independently recomputed duration minutes for each case.
- Unique monthly KPI months, percentage bounds, nonnegative values and separate source provenance.
- Source-derived aggregate counts and average sample resolution time, saved as a JSON artifact.

`tests/test_itops_console.py` uses negative fixtures to prove malformed data fails. Every row embedded in the interactive HTML must exactly match its original CSV, and the UI must avoid external JavaScript, API calls and unsafe `innerHTML` rendering.

## Automated safe script validation

[GitHub Actions](../.github/workflows/validate-itops.yml) runs:

- Python 3.11/3.12: standalone integrity checks and regression tests.
- PowerShell syntax parsing for selected Help Desk, IT Operations and Outlook support `.ps1`/`.psm1` files, using the language parser only. **No scripts are executed**, and no AD, Exchange, Intune or Windows host connection is created.
- Bash `-n` syntax checks for selected IT Ops/Help Desk scripts without executing their commands.
- SHA-256 verified Gitleaks scan of full Git history, which fails on potential credential findings.

This phase does **not** claim that all 2,451 repository files are tested, that nested legacy tests have been reconciled, that Pester integration or remote tenant validation was performed, or that the portfolio's separate real-tenant investigation was reproduced. The deliberately narrow script paths avoid inadvertently executing administrative actions on a hosted runner.

## Publication and additional checks

Before publication, review the HTML in desktop and mobile browsers, scan for accessibility issues, independently review scripts with elevated privileges or state-changing behavior, and create intentional mocked Pester tests for safe pure functions. Separately validate historical archive claims and any missing cross-file mappings. CI passing is evidence for these bounded automated checks only; it does not certify secure deployment, live system administration, or production service outcomes.
