# Microsoft 365 & Entra ID — Identity and Access Incident Investigation

**Hands-on portfolio case study | 20 October 2026 | Microsoft Entra ID · Microsoft Graph · PowerShell 7.5.4**

> **Evidence integrity:** This project combines an explicitly **simulated** employee service-access ticket with **real, read-only** administration and API checks performed in a personal practice tenant. No employee outage was reproduced, no license was assigned, and no service restoration was demonstrated. All screenshots are edited to remove browser tabs and obscure account identifiers. No secrets, tokens, or raw unredacted images are included.

## Executive summary

A fictional employee reported being unable to access Outlook, Teams and SharePoint. I followed a structured identity-and-access triage: account status, privileged roles, interactive sign-in logs, and product licensing. I then installed Microsoft Graph PowerShell, connected using delegated `User.Read`, investigated an unexpectedly empty `Get-MgContext` account field, and successfully retrieved the signed-in profile with a direct Graph `/me` request.

**Observed:** account enabled; one directly assigned Global Administrator role; successful Azure Portal interactive sign-in (error code `0`); no Microsoft 365 product licenses assigned; Microsoft.Graph SDK `2.41.2` installed; `/me` API request succeeded. **Not established:** cause of a real Outlook/Teams/SharePoint failure; service restoration; whether a license was required for a particular test workload; root cause of the context anomaly.

## Business relevance

- **M365 Administrator:** identity inspection, licensing checks, privilege awareness and audit-ready documentation.
- **IT Analyst:** evidence-led ticket triage, hypothesis tracking, impact assessment and escalation.
- **Cloud Support Analyst:** delegated authentication, PowerShell SDK setup, Graph REST diagnostics and API fallback.

## Investigation workflow

`Reported access problem (simulated) → Verify account state → Review role → Check sign-in events → Review licenses → Verify Graph connectivity → Record findings → Recommend next steps`

## Findings and interpretation

| Control | Observed evidence | Interpretation | Confidence |
|---|---|---|---|
| User status | Enabled | Disabled account not supported as explanation | High |
| Role | Global Administrator, direct assignment | Privileged account; apply least privilege | High |
| Interactive sign-in | Azure Portal success, error 0, 24h view | Authentication worked for this specific application/event | High |
| Licensing | No license assignments found | Potential explanation for unavailable licensed workloads; **not proof of outage** | High for fact; low for causation |
| Graph SDK | Microsoft.Graph 2.41.2 | SDK installation verified | High |
| Delegated Graph connection | Connection welcome message | Authentication flow reported success | High |
| Context | Account/TenantId/Scopes selection showed empty fields | Unexpected context behavior; underlying cause undetermined | High for observation |
| `Get-MgUser` | Empty `UserId` parameter error | Command failed because context account was empty | High |
| Graph REST `/me` | User profile properties returned | Authenticated Graph API call succeeded | High |

## Repository contents

| Location | Purpose |
|---|---|
| `docs/INC-2026-1042.md` | Formal support incident, timeline, hypotheses, decision log, verification and closure criteria |
| `docs/TROUBLESHOOTING_RUNBOOK.md` | Reusable M365 identity, sign-in and licensing runbook |
| `docs/SECURITY_AND_GOVERNANCE.md` | Least privilege, privileged identity and privacy controls |
| `docs/VALIDATION_AND_LIMITATIONS.md` | Evidence matrix, assumptions, acceptance tests and unresolved items |
| `docs/INTERVIEW_STORY.md` | Concise STAR interview narrative, truthful resume bullet suggestions |
| `docs/EVIDENCE_INDEX.md` | Screenshot-to-claim mapping and redaction notes |
| `scripts/ReadOnly-M365IdentityDiagnostics.ps1` | Defensive, read-only Graph profile/context checks; no write actions |
| `scripts/Test-GraphConnectivity.ps1` | Isolated Graph REST `/me` test with error handling |
| `data/sample_ticket.csv` | Synthetic ticket record for demonstration |
| `diagrams/workflow.mmd` | Incident triage decision flow |
| `evidence/screenshots/` | Cropped, privacy-redacted original training captures |

## Safe reproduction

**Requirements:** PowerShell 7+, Microsoft Graph PowerShell SDK, authorized Entra tenant, permission to inspect your own account. Review tenant policy before consenting to scopes. No paid license required to read account metadata, but features/log access vary by tenant.

```powershell
Install-Module Microsoft.Graph -Scope CurrentUser -Repository PSGallery
Connect-MgGraph -Scopes 'User.Read'
./scripts/Test-GraphConnectivity.ps1
./scripts/ReadOnly-M365IdentityDiagnostics.ps1
```

The scripts are **read-only** and intentionally do not assign licenses, reset passwords, revoke sessions, or modify tenant settings. An administrative role does not automatically grant Microsoft Graph delegated OAuth scopes.

## Verification standard

A ticket may be marked **Resolved** only after the affected service is successfully retested with the user, or after equivalent validated proof of restoration. This simulated ticket remains **Investigation documented / pending real-service verification**.

## Engineering quality and enterprise-ready artifacts

This release adds an **offline unit-test suite**, **GitHub Actions quality workflow**, **PowerShell syntax validation**, **least-privilege operational runbooks**, **incident priority and escalation matrix**, **root-cause decision tree**, **Graph context diagnostic playbook**, **privacy publication policy**, **change-control template**, and **recruiter walkthrough**. These are engineering artifacts and proposed procedures, **not evidence of additional tenant actions or a restored incident**.

| Added resource | Purpose |
|---|---|
| `.github/workflows/quality.yml` | Offline CI: Python checks, PowerShell parsing, Pester tests |
| `tests/GraphDiagnostics.Tests.ps1` | Six isolated Pester cases (no Graph authentication) |
| `tests/test_portfolio.py` | Offline repository and privacy smoke checks |
| `scripts/GraphDiagnostics.Core.psm1` | Pure functions for error classification and context/profile interpretation |
| `docs/ESCALATION_AND_SLA.md` | Illustrative incident severity, RACI, handoff, closure gates |
| `docs/ROOT_CAUSE_DECISION_TREE.md` | App-specific access troubleshooting flowchart |
| `docs/GRAPH_CONTEXT_TROUBLESHOOTING.md` | Repeatable diagnostics for unresolved Graph context anomaly |
| `docs/PRIVACY_AND_PUBLICATION.md` | Public GitHub release checklist |
| `docs/TESTING_AND_ACCEPTANCE.md` | Test layers, how to run, honest acceptance boundaries |
| `docs/CHANGE_CONTROL_TEMPLATE.md` | Proposed, unexecuted remediation and rollback plan |
| `docs/RECRUITER_GUIDE.md` | Truthful recruiter narrative and resume bullet options |

**Run offline quality checks:** `python3 -m unittest discover -s tests -p "test_*.py" -v`. PowerShell Pester and parser checks are configured for GitHub Actions; do not claim a CI pass until a workflow actually executes.

## Next enhancements

1. Reproduce a licensed-service access failure in a separate disposable lab account if an appropriate test license is available.
2. Compare application-specific sign-in events and Conditional Access details where licensed/authorized.
3. Investigate SDK context discrepancy in a new session and record module/version/environment behavior.
4. Add a separate least-privilege non-admin practice account; avoid changing the only Global Administrator account.

## Sources

- [Microsoft Graph PowerShell overview](https://learn.microsoft.com/powershell/microsoftgraph/overview)
- [Get-MgContext](https://learn.microsoft.com/powershell/module/microsoft.graph.authentication/get-mgcontext)
- [Microsoft Graph `/me` endpoint](https://learn.microsoft.com/graph/api/user-get)
- [Microsoft Entra sign-in logs](https://learn.microsoft.com/entra/identity/monitoring-health/concept-sign-ins)
- [Microsoft 365 licensing](https://learn.microsoft.com/microsoft-365/admin/manage/assign-licenses-to-users)

**Scope:** independent training case study; not an endorsement by Microsoft and not evidence of paid employment or a production incident.
