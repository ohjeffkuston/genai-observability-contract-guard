"""Policy engine for production GenAI evaluation and telemetry contracts."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

REQUIRED_ATTRIBUTES = {
    "gen_ai.operation.name",
    "gen_ai.provider.name",
    "gen_ai.request.model",
    "gen_ai.response.model",
    "gen_ai.prompt.name",
    "service.name",
    "deployment.environment.name",
}
REQUIRED_METRICS = {"request.duration", "time_to_first_token", "input_tokens", "output_tokens", "error_rate"}
REQUIRED_EVALUATIONS = {"quality", "safety", "groundedness"}


def load_contract(path: str | Path) -> dict[str, Any]:
    with Path(path).open(encoding="utf-8") as handle:
        value = yaml.safe_load(handle)
    if not isinstance(value, dict):
        raise ValueError("contract must be a YAML mapping")
    return value


def _finding(rule: str, severity: str, passed: bool, message: str) -> dict[str, Any]:
    return {"rule": rule, "severity": severity, "passed": passed, "message": message}


def analyze_contract(contract: dict[str, Any]) -> dict[str, Any]:
    telemetry = contract.get("telemetry", {})
    privacy = contract.get("privacy", {})
    evaluation = contract.get("evaluation", {})
    operations = contract.get("operations", {})
    findings: list[dict[str, Any]] = []

    attributes = set(telemetry.get("attributes", []))
    missing_attributes = sorted(REQUIRED_ATTRIBUTES - attributes)
    findings.append(_finding("semantic-attributes", "block", not missing_attributes, f"Missing required attributes: {missing_attributes}" if missing_attributes else "Required OpenTelemetry and service attributes are declared."))

    metrics = set(telemetry.get("metrics", []))
    missing_metrics = sorted(REQUIRED_METRICS - metrics)
    findings.append(_finding("operational-metrics", "block", not missing_metrics, f"Missing operational metrics: {missing_metrics}" if missing_metrics else "Latency, token, and error metrics are declared."))

    eval_names = {item.get("name") for item in evaluation.get("signals", []) if isinstance(item, dict)}
    missing_evals = sorted(REQUIRED_EVALUATIONS - eval_names)
    findings.append(_finding("evaluation-coverage", "block", not missing_evals, f"Missing evaluation signals: {missing_evals}" if missing_evals else "Quality, safety, and groundedness evaluations are declared."))

    linked = all(item.get("trace_link") is True and item.get("model_version") is True and item.get("prompt_version") is True for item in evaluation.get("signals", []) if isinstance(item, dict)) and bool(evaluation.get("signals"))
    findings.append(_finding("evaluation-linkage", "block", linked, "Every evaluation signal links to a trace, model version, and prompt version."))

    content_capture = privacy.get("capture_prompt_or_response_content", True)
    findings.append(_finding("content-capture-default", "block", content_capture is False, "Prompt and response content capture is disabled by default."))

    redaction = privacy.get("redaction", {})
    redaction_ok = redaction.get("enabled") is True and {"email", "phone", "credential"}.issubset(set(redaction.get("classes", [])))
    findings.append(_finding("pii-redaction", "block", redaction_ok, "Redaction covers email, phone, and credential material."))

    sample_rate = telemetry.get("sample_rate", 0)
    sampling_ok = isinstance(sample_rate, (int, float)) and 0 < sample_rate <= 1
    findings.append(_finding("bounded-sampling", "review", sampling_ok, "Sampling is explicitly bounded between zero and one."))

    retention = int(privacy.get("retention_days", 0) or 0)
    findings.append(_finding("bounded-retention", "review", 1 <= retention <= 30, f"Telemetry retention is {retention} days; policy allows 1-30."))

    slo = operations.get("slo", {})
    slo_ok = 0.90 <= float(slo.get("availability", 0) or 0) < 1 and float(slo.get("p95_latency_ms", 0) or 0) > 0 and float(slo.get("quality_score", 0) or 0) > 0
    findings.append(_finding("service-level-objectives", "block", slo_ok, "Availability, latency, and quality SLOs are defined."))

    owner_ok = bool(operations.get("alert_owner")) and bool(operations.get("runbook_url"))
    findings.append(_finding("alert-ownership", "review", owner_ok, "Alerts have an owner and runbook."))

    baseline_ok = bool(evaluation.get("baseline", {}).get("dataset_version")) and bool(evaluation.get("baseline", {}).get("model_version"))
    findings.append(_finding("versioned-baseline", "block", baseline_ok, "The evaluation baseline pins dataset and model versions."))

    rollback_ok = operations.get("rollback", {}).get("enabled") is True and bool(operations.get("rollback", {}).get("trigger"))
    findings.append(_finding("rollback-response", "review", rollback_ok, "A human-approved rollback trigger is declared."))

    failed_block = sum(1 for finding in findings if not finding["passed"] and finding["severity"] == "block")
    failed_review = sum(1 for finding in findings if not finding["passed"] and finding["severity"] == "review")
    decision = "BLOCK" if failed_block else ("REVIEW" if failed_review else "PASS")
    score = round(100 * sum(1 for finding in findings if finding["passed"]) / len(findings))
    return {"service": contract.get("service", "unnamed"), "decision": decision, "score": score, "findings": findings}
