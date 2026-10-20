# Verification and acceptance plan

## Test layers

| Layer | Tool | Scope | Requires live tenant? |
|---|---|---|---|
| Documentation & privacy smoke checks | Python `unittest` | Required artifacts, screenshot count, synthetic disclosure, common secret patterns | No |
| PowerShell parser check | PowerShell AST parser | Syntax of `.ps1` and `.psm1` files | No |
| Diagnostic function unit tests | Pester 5 | Failure classification and Graph context/profile summary | No |
| Real Graph profile check | `Invoke-MgGraphRequest` | Delegated `/me` | Yes, optional; already observed in lab |
| Microsoft 365 workload restoration | User/app retest | End-to-end business outcome | Yes; **not performed** |

## How to run locally

```bash
python3 -m unittest discover -s tests -p 'test_*.py' -v
```

```powershell
Install-Module Pester -MinimumVersion 5.0 -Scope CurrentUser
Invoke-Pester -Path ./tests/GraphDiagnostics.Tests.ps1 -CI
```

GitHub Actions runs the offline gates on push and pull request. CI does **not** request tenant credentials or perform live Graph calls.

## Acceptance boundaries

- **Documentation complete:** evidence and simulated scope labeled, root cause remains undetermined.
- **Automation tested:** offline helpers pass Pester; syntax parser succeeds in CI.
- **Service restored:** **not met**. Requires a reproduced workload failure, approved remediation, and successful retest.

Do not claim the CI workflow passed in GitHub until it has actually run there. Local Python test results may be documented separately.
