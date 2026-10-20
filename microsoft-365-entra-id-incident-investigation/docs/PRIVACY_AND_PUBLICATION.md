# Public GitHub privacy and evidence policy

## Source and publication boundaries

Original screenshots from the practice session are **not included**. Published screenshots are derivatives with browser tabs removed and opaque masking over account headers, user identifiers, tenant information, local filesystem names, request IDs and profile output. Some evidence is deliberately heavily obscured: the incident record and command transcript provide the interpretation without exposing personal identifiers.

## Mandatory manual release checklist

- [ ] Inspect every screenshot at 100% zoom for names, email addresses, URLs, tenant IDs, GUIDs, correlation/request IDs, IP addresses, user IDs and device names.
- [ ] Check screenshots for browser tabs, address bar, desktop notifications and private filenames.
- [ ] Ensure redaction uses opaque pixels (not blur or transparency) and that original screenshots are absent.
- [ ] Check `git status`, `git log` and staged files for accidental raw evidence.
- [ ] Run offline tests and inspect any generated files before publishing.
- [ ] Confirm no access tokens, refresh tokens, client secrets, certificates or exported credentials appear in any artifact.
- [ ] Never publish real employee data or confidential tenant policies.

## Evidence authenticity

Screenshots are edited evidence from the actual training session, not mockups. Editing may remove context, so every claim is paired with a written observation and its limitations. Test data and scenarios in the repository are explicitly synthetic.

## If sensitive information is accidentally committed

Remove the material from the working tree, revoke/rotate affected secrets immediately, and follow GitHub guidance for removing sensitive data from history. A later deletion commit alone does not erase earlier versions.
