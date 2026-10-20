# Identity and Microsoft 365 access diagnostic decision tree

```mermaid
flowchart TD
  A[Collect exact error, app, timestamp and impact] --> B{Account enabled?}
  B -->|No| C[Confirm authorized account-state remediation]
  B -->|Yes| D{Matching app sign-in event?}
  D -->|No| E[Confirm tenant, identity, client, event time and sign-in type]
  D -->|Yes| F{Authentication succeeded?}
  F -->|No| G[Inspect failure code, MFA, CA, device, risk and network]
  F -->|Yes| H{Application access works?}
  H -->|Yes| I[Validate with user and document evidence]
  H -->|No| J{License or service plan required and assigned?}
  J -->|No| K[Verify entitlement and seek approved assignment]
  J -->|Yes| L[Inspect workload health, app authorization and provisioning]
  C --> M[Retest affected workload]
  G --> M
  K --> M
  L --> M
  M --> N{User confirms restoration?}
  N -->|No| O[Escalate with complete diagnostic packet]
  N -->|Yes| P[Resolve ticket with verification evidence]
```

## Key interpretation rules

- An **Azure Portal** success is not proof that **Teams**, **SharePoint**, or **Exchange Online** sign-in succeeds.
- A missing license may explain a workload entitlement failure, but not necessarily an Entra authentication failure.
- A **Global Administrator** directory role does not automatically include Exchange/Teams licensing or Graph delegated OAuth scopes.
- A Graph `/me` success validates that specific delegated REST request, not every SDK cmdlet or Microsoft 365 workload.
- Absence of a failed event in a limited log view does not prove no failures exist.
