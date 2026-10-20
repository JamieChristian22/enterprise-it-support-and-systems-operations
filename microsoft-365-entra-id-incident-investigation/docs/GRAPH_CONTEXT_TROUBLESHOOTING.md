# Microsoft Graph PowerShell context anomaly — diagnostic playbook

## Observed evidence

`Connect-MgGraph -Scopes 'User.Read'` displayed a successful delegated connection. `Get-MgContext | Select-Object Account,TenantId,Scopes` displayed column headings without populated values. The dependent `Get-MgUser -UserId (Get-MgContext).Account` call failed with an empty-string parameter error. `Invoke-MgGraphRequest -Method GET -Uri 'https://graph.microsoft.com/v1.0/me'` returned profile properties successfully.

**Interpretation:** the REST request worked; the cause of the context property behavior was **not established**. Do not claim a verified SDK defect, credential failure, or tenant misconfiguration.

## Safe reproduction steps (authorized account only)

1. Open a fresh PowerShell 7 session and record `Get-Module Microsoft.Graph* -ListAvailable | Select-Object Name,Version` (redact paths).
2. Run `Get-MgContext | Format-List AuthType,Account,TenantId,Scopes,ContextScope` and record whether a context object exists. Do **not** publish the raw tenant ID.
3. Compare `Get-MgContext | Select-Object Account,TenantId,Scopes` with `Get-MgContext | Format-List *` locally to distinguish formatting from absent values.
4. With authorization, reauthenticate with `Connect-MgGraph -Scopes 'User.Read' -ContextScope Process -NoWelcome` and retest in the same session.
5. Test the delegated endpoint independently: `Invoke-MgGraphRequest -Method GET -Uri 'https://graph.microsoft.com/v1.0/me'`.
6. If context is still anomalous, collect a sanitized module-version report and error category; escalate without publishing access tokens, IDs, or user details.

## Error categories

| Category | Common symptom | Next safe action |
|---|---|---|
| Authentication | HTTP 401 | Check active connection and token renewal; never print token |
| Authorization | HTTP 403 | Check least-privilege delegated scopes and consent |
| Throttling | HTTP 429 | Honor `Retry-After`, exponential backoff |
| Connectivity | DNS/timeout | Check proxy, DNS, firewall, service health |
| Context missing | Empty `Account` / `UserId` | Inspect context object; use `/me` as limited fallback |
| License / workload | Portal works, licensed app unavailable | Check workload entitlement and app-specific logs |

## Acceptance criteria

- **Verified:** `/me` returns an authorized test user's profile with no secrets printed.
- **Not verified:** account properties in `Get-MgContext` become populated in a fresh session.
- **Do not overstate:** a successful `/me` does not fix the original simulated Microsoft 365 access issue.
