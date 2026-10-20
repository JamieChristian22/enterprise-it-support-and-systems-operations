# Runbook — Microsoft 365 Identity and Application Access

## Intake and severity

Capture affected user (in private ticket system), application, exact error, first observed time/timezone, scope (# affected users), device, network, client/browser, business impact and recent changes. Escalate widespread outages or compromised accounts immediately according to organization policy. Never request a user's password or MFA code.

## Read-only triage decision tree

1. **Account state:** Confirm user exists, is enabled, and is not deleted. If disabled, validate authorization and cause before proposing changes.
2. **Authentication:** Inspect interactive and non-interactive sign-in logs for the **affected application and timeframe**. Record status, error code, authentication requirement, Conditional Access result, correlation ID and client application where accessible. Successful Azure Portal login does not establish Outlook success.
3. **Authorization and entitlement:** Confirm product assignment, service-plan enablement, group-based licensing, provisioning delay and usage location where applicable. Lack of license can prevent access to licensed workloads but not necessarily Entra sign-in.
4. **Conditional Access and MFA:** Check policy outcome and MFA details. Do not weaken MFA or bypass policies to make a ticket appear resolved.
5. **Application path:** Test browser vs client, service health, network/DNS, cached tokens, client versions and relevant service diagnostics. Avoid destructive resets without approval.
6. **Resolution:** Implement only approved changes, verify actual app functionality, obtain user confirmation and document evidence.

## Example branching

| Observation | Next action |
|---|---|
| User disabled | Validate intentional disablement and authorized re-enable workflow |
| Sign-in failure with error | Use exact code, app and Conditional Access/MFA details |
| Sign-in succeeds, app access denied | Inspect licensing, app role/permissions, service provisioning |
| No license assigned | Verify entitlement and business need before requesting assignment |
| No event found | Confirm timezone, event type, tenant and app; collect correlation ID |
| Graph context account empty | Inspect full context and use authorized `/me` API as independent check |

## Evidence quality

Capture redacted screenshots, relevant commands, result interpretation, timestamp/timezone, alternative explanations, and what was **not** tested. Do not publish full UPNs, IDs, IPs, session details, tokens or browser tabs.

## Escalation handoff template

**Summary:** [affected app / exact symptom]  
**Impact:** [users, urgency, business impact]  
**Confirmed:** [account state, exact app sign-in status, licensing]  
**Excluded:** [only what evidence excludes]  
**Open questions:** [hypotheses]  
**Actions taken:** [read-only vs approved changes]  
**Requested action:** [specific team and reason]  
**Verification plan:** [expected successful retest]
