# Enterprise incident response: priority, escalation, and SLAs

**Scenario:** Simulated single-user access problem. **No real business impact or contractual SLA was observed.** All durations below are *illustrative training targets*, not a claim about any employer's policy.

## Impact / urgency matrix

| Impact | Urgency | Example | Illustrative priority | Initial response target |
|---|---|---|---|---|
| Enterprise-wide | Critical | Most employees cannot authenticate | P1 | 15 minutes |
| Department-wide | High | Many users blocked from business-critical workflow | P2 | 30 minutes |
| Single user | Normal | One employee cannot use a licensed app | P3 | 4 business hours |
| Cosmetic or nonblocking | Low | Optional profile field incorrect | P4 | 1 business day |

A single user with a time-critical regulated workflow may warrant higher priority. Confirm scope and urgency before assigning priority.

## RACI and handoffs

| Activity | Service desk (L1) | Identity admin (L2) | M365 service owner | Security / IAM |
|---|---|---|---|---|
| Collect symptom, error, timestamp, device | Responsible | Consulted | Informed | Informed |
| Inspect enabled status and app-specific sign-ins | Responsible if authorized | Accountable | Consulted | Consulted |
| Review licensing entitlement | Responsible if authorized | Consulted | Accountable | Informed |
| Approve role / Conditional Access changes | Informed | Responsible | Consulted | Accountable |
| Validate restoration and user confirmation | Responsible | Consulted | Accountable | Informed |

## Escalation packet (minimum)

- Ticket ID, impact and priority rationale; time zone and timestamps
- Exact app name, error code, correlation ID (internal-only), device and network context
- Redacted sign-in log status and Conditional Access outcome
- License and service-plan entitlement findings
- Tests performed, negative results, and no-change confirmation
- Decision owner, change request number if applicable, next update due

## Operational safeguards

Do not reset passwords, remove the last Global Administrator, disable Conditional Access, grant broad OAuth scopes, or purchase/assign licenses merely to complete a lab. For any write operation, require a separate approved change, least-privilege operator, backup/recovery strategy, and post-change validation.

## Closure gates

A ticket can move from **Investigating** to **Resolved** only with verified affected-workload access and appropriate user confirmation. Close only after evidence and any change record are linked. This exercise remains **Investigation documented**.
