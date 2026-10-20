# Security, Least Privilege and Governance Review

## Risk register

| Risk | Evidence | Severity (illustrative) | Recommendation |
|---|---|---|---|
| Broad privilege | Practice account directly assigned Global Administrator | High | Use dedicated privileged identity, least-privilege roles, MFA and PIM where available |
| Single privileged user | One visible account in tenant | High for recoverability | Establish approved break-glass strategy before role changes; do not lock out tenant |
| License gap | No license assignments | Medium operational concern | Validate service needs and entitlement; do not assume root cause |
| Sensitive screenshots | Original captures show identifiers and browser context | Medium | Crop tabs and mask identities before publishing |
| Excessive Graph scopes | User.Read sufficient for self-profile | Low in this lab | Request minimum delegated scopes; review consent and tenant policy |

## Controls demonstrated

- Read-only inspection; no user disablement, password reset, role change, license assignment or session revocation.
- No tokens or credentials stored in repository.
- Distinction between Azure Portal authentication and separate M365 workload authorization.
- Explicit simulation labeling, evidence provenance and unresolved hypotheses.

## Production recommendations

Use separate standard and privileged accounts, phishing-resistant MFA where possible, Conditional Access with change management, PIM/JIT privilege, audit retention, recovery access, ticket-based approval and periodic access review. Administrative Graph API scopes and directory roles are distinct controls.

## Screenshot sanitization

Screenshots are derivative images from the training conversation, cropped to remove browser tabs, browser chrome and desktop surroundings, with broad privacy masks. Some masks intentionally obscure content to prevent inadvertent identifier disclosure. The ZIP contains **no raw originals**. Review every screenshot before public upload, because manual visual redaction cannot guarantee removal of every indirect identifier. Keep originals private. Do not interpret obscured areas as evidence.
