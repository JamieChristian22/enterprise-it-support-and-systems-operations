# Interview and Resume Translation

## STAR narrative (practice project; not employment)

**Situation:** In a self-directed Microsoft 365 administration lab, I investigated a simulated report that Outlook, Teams and SharePoint were inaccessible.  
**Task:** Establish which identity, authentication, licensing or API layers could explain the report without changing tenant configuration.  
**Action:** I inspected account enablement and direct directory roles, reviewed the latest interactive Azure Portal sign-in, confirmed no assigned product licenses, installed Microsoft Graph PowerShell 2.41.2, authenticated with delegated `User.Read`, diagnosed an empty context-dependent user lookup, and successfully queried the `/me` endpoint.  
**Result:** Produced an evidence-backed incident report and escalation runbook; distinguished a plausible licensing issue from a proven root cause and documented the unresolved Graph context anomaly.

## Resume bullet options (truthful)

- Conducted a self-directed Microsoft Entra ID access-troubleshooting lab, reviewing account state, privileged role assignments, interactive sign-in logs and Microsoft 365 licensing; documented findings in an ITIL-style simulated incident report.
- Installed Microsoft Graph PowerShell 2.41.2 and performed delegated read-only API diagnostics, successfully retrieving user profile data through Graph REST after identifying an empty context-dependent user lookup.
- Created reusable troubleshooting, evidence-handling and escalation documentation emphasizing least privilege, service-specific validation and secure screenshot redaction.

## Interview questions to rehearse

**Q: Why didn't a successful Azure Portal sign-in resolve the ticket?**  
A: Authentication to Azure Portal is one application-specific event. Microsoft 365 workloads may require distinct service plans and access checks.

**Q: Was the missing license the root cause?**  
A: No. It was a strong entitlement finding and a plausible hypothesis, but I didn't reproduce or validate a target-app failure.

**Q: Why use `/me`?**  
A: The selected `Get-MgContext` properties were empty, so the dependent `Get-MgUser` call received an empty user ID. A direct delegated `/me` request avoided that dependency and confirmed the Graph API could return my profile.

**Q: What would you do next in production?**  
A: Collect the target app's exact error and timestamp, inspect its sign-in and Conditional Access events, confirm license entitlements, obtain change approval and verify the user's actual service access before closure.
