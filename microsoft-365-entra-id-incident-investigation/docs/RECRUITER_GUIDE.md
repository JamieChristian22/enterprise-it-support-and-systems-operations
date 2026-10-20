# Recruiter and hiring-manager guide

## What this demonstrates

- **IT Analyst / Service Desk:** incident intake, read-only identity triage, sign-in-log interpretation, evidence and escalation.
- **Microsoft 365 Administrator:** directory account checks, license inventory, privileged role awareness and governance.
- **Cloud Support Analyst:** PowerShell 7, Graph SDK installation, delegated API access, error handling and a REST fallback.

## 60-second walkthrough

"I used a simulated Microsoft 365 user-access ticket to practice a real Entra ID investigation in my own authorized tenant. I confirmed the account was enabled, found a directly assigned Global Administrator role, reviewed a successful Azure Portal sign-in, and confirmed no M365 licenses were assigned. I installed Microsoft Graph PowerShell and found an unusual context result: the account property was empty, causing a dependent cmdlet to fail. I verified delegated API access independently with Graph `/me`, then documented what was verified and what remained unknown. The case study includes an escalation runbook, privacy-redacted evidence, offline tests and a CI workflow. I did not claim the fictional employee outage was restored." 

## Truthful resume bullets

- Conducted a hands-on Entra ID identity-access investigation, examining account state, privileged roles, sign-in records and Microsoft 365 licensing in a practice tenant.
- Installed and used Microsoft Graph PowerShell 2.41.2; diagnosed an empty context-account error and validated delegated profile access via the Graph `/me` endpoint.
- Produced an evidence-indexed incident report, escalation runbook, privacy-redacted screenshots and offline PowerShell testing artifacts.

## Interview follow-ups

**Why did the Graph cmdlet fail?** It received an empty `UserId` because the selected context account was empty; the underlying reason for the empty context was not proven.

**Was missing licensing the root cause?** No. It was a confirmed finding and plausible entitlement hypothesis, but no real target-workload failure was reproduced.

**Would you remove Global Administrator?** Not without change approval, recovery access, and a safe least-privilege transition plan.
