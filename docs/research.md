# Demand and technical validation

Checked 2026-11-07.

## Authoritative sources

- [OpenTelemetry semantic conventions](https://opentelemetry.io/docs/specs/semconv/) standardize span, metric, and event names and attributes.
- [OpenTelemetry GenAI attributes](https://opentelemetry.io/docs/specs/semconv/registry/attributes/gen-ai/) include operation, provider, model, token, response, workflow, and evaluation fields.
- [OpenTelemetry event guidance](https://opentelemetry.io/docs/specs/semconv/general/events/) calls for structured timestamps, severity, reusable attributes, and explicit treatment of sensitive or large fields.
- [Google Cloud model monitoring](https://docs.cloud.google.com/gemini-enterprise-agent-platform/machine-learning/model-monitoring/monitor-explainable-ai) describes training-serving skew and prediction drift as production monitoring concerns.

## Live demand signal

Current remote U.S. ML-platform and platform-engineering postings reviewed on 2026-11-07 repeatedly asked for evaluation platforms, reproducibility, model monitoring, Python, Kubernetes, cloud-native orchestration, data quality, internal tooling, and production reliability. Salary examples in the surfaced market ranged from $150,000 to $290,000 base for platform and ML-platform scopes. The postings were used only to validate demand; application eligibility was assessed separately.

## Rationale

The project is not a generic AI demonstration. It addresses the enterprise failure mode where infrastructure telemetry, model evaluations, and privacy controls are fragmented, preventing reliable ship/no-ship and incident decisions.
