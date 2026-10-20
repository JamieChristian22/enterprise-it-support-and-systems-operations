# Validation, Evidence Integrity and Limitations

## Claim-to-evidence matrix

| Claim | Screenshot | Strength | Caveat |
|---|---|---|---|
| One user visible | 01 | Direct | Snapshot, not tenant inventory audit |
| Account enabled | 02 | Direct | Practice user only |
| Direct Global Administrator | 03 | Direct | Not a security audit of all principals |
| Azure Portal sign-in succeeded | 04 | Direct | Not Outlook, Teams or SharePoint |
| No assigned product licenses | 05 | Direct | Does not alone establish incident cause |
| Graph SDK installed | 06 | Direct | Local PowerShell environment |
| Graph delegated connection message | 07 | Direct | Context later lacked account fields |
| Empty context selected properties | 08 | Direct | Underlying cause unknown |
| Context-based user lookup failed | 09 | Direct | Empty argument; not API denial |
| Graph `/me` returned profile | 10 | Direct | Does not prove app service availability |

## Quality gates

- [x] Real vs simulated explicitly distinguished
- [x] Observations separated from inferences
- [x] Read-only API diagnostics included
- [x] Failed command preserved, not hidden
- [x] Sensitive browser chrome removed from shared images
- [x] No secrets included in documentation
- [x] Troubleshooting runbook and escalation workflow
- [x] Formal ticket and acceptance criteria
- [ ] Independent live reproduction of Outlook/Teams/SharePoint failure
- [ ] User-confirmed service restoration
- [ ] Validated explanation for empty SDK context
- [ ] Automated CI against disposable lab tenant (not appropriate without tenant and credentials)

## Evidence collection notes

Screenshot filenames are curated labels rather than native timestamps. Source images were captured in the same 2026-10-20 training session. The terminal evidence shows commands and output, but some identity-bearing values are intentionally hidden. Screenshots are **not** cryptographic proof of production operations.

## Why not close as resolved?

The simulation has no actual affected employee or reproducible target-app failure. A successful `/me` API call proves one Graph endpoint worked, not that Outlook/Teams/SharePoint were restored. The report closes **the exercise**, not **the incident**.
