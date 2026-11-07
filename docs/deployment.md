# Safe deployment guidance

1. Add one contract per production GenAI service.
2. Run the guard in pull requests before collector, dashboard, or alert configuration changes.
3. Start REVIEW-only, baseline failures, and document approved exceptions with owners and expiry.
4. Enforce BLOCK after teams have migrated contracts.
5. Send synthetic requests to verify traces, metrics, evaluations, and version linkage arrive together.
6. Test redaction with seeded PII and credential-like values; never use real secrets.
7. Run controlled quality-regression exercises and measure alert and rollback decision time.

Use least-privilege CI permissions, pin dependencies and images, sign releases, and keep production rollout or rollback behind human approval. Export only aggregated non-sensitive compliance metrics.
