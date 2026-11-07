# To: ohjeffkuston@yahoo.ca
# Subject: Day 24 — GenAI Evaluation Observability Contract Guard

Day 24 delivers a production-focused observability contract for GenAI services.

The guard connects OpenTelemetry-aligned service and GenAI attributes with evaluation signals, model and prompt versions, latency/token/error metrics, privacy controls, SLOs, ownership, baselines, and rollback response. It is deterministic and offline; AI may explain findings but cannot override policy.

Deployment: run it in pull requests before collector and dashboard changes, begin in report-only mode, migrate contracts, then enforce blocking rules. Verify runtime delivery with synthetic requests, seed synthetic PII to test redaction, and run controlled quality-regression exercises.

Learning: the project shows how SRE telemetry and model-quality operations fit into one platform contract, with explicit trade-offs around sampling, retention, storage, privacy, and rare-event detection.

Interview positioning: discuss the production failure mode, cross-signal correlation, fail-closed privacy defaults, deterministic policy, CI evidence, measurable incident outcomes, and human approval boundaries.

Repository: https://github.com/ohjeffkuston/genai-observability-contract-guard
