from copy import deepcopy

import yaml

from observability_contract_guard.analyzer import analyze_contract


def contract():
    with open("samples/compliant-contract.yaml", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def test_compliant_contract_passes():
    report = analyze_contract(contract())
    assert report["decision"] == "PASS"
    assert report["score"] == 100


def test_missing_semantic_attribute_blocks():
    item = contract(); item["telemetry"]["attributes"].remove("gen_ai.operation.name")
    assert analyze_contract(item)["decision"] == "BLOCK"


def test_missing_metric_blocks():
    item = contract(); item["telemetry"]["metrics"].remove("error_rate")
    assert analyze_contract(item)["decision"] == "BLOCK"


def test_missing_evaluation_signal_blocks():
    item = contract(); item["evaluation"]["signals"].pop()
    assert analyze_contract(item)["decision"] == "BLOCK"


def test_unlinked_evaluation_blocks():
    item = contract(); item["evaluation"]["signals"][0]["trace_link"] = False
    assert analyze_contract(item)["decision"] == "BLOCK"


def test_content_capture_blocks():
    item = contract(); item["privacy"]["capture_prompt_or_response_content"] = True
    assert analyze_contract(item)["decision"] == "BLOCK"


def test_missing_redaction_class_blocks():
    item = contract(); item["privacy"]["redaction"]["classes"].remove("credential")
    assert analyze_contract(item)["decision"] == "BLOCK"


def test_invalid_sampling_requires_review():
    item = contract(); item["telemetry"]["sample_rate"] = 2
    assert analyze_contract(item)["decision"] == "REVIEW"


def test_long_retention_requires_review():
    item = contract(); item["privacy"]["retention_days"] = 90
    assert analyze_contract(item)["decision"] == "REVIEW"


def test_missing_quality_slo_blocks():
    item = contract(); item["operations"]["slo"]["quality_score"] = 0
    assert analyze_contract(item)["decision"] == "BLOCK"


def test_missing_owner_requires_review():
    item = contract(); item["operations"]["alert_owner"] = ""
    assert analyze_contract(item)["decision"] == "REVIEW"


def test_missing_baseline_blocks():
    item = contract(); item["evaluation"]["baseline"].pop("dataset_version")
    assert analyze_contract(item)["decision"] == "BLOCK"


def test_disabled_rollback_requires_review():
    item = contract(); item["operations"]["rollback"]["enabled"] = False
    assert analyze_contract(item)["decision"] == "REVIEW"


def test_block_precedes_review():
    item = deepcopy(contract()); item["operations"]["alert_owner"] = ""; item["privacy"]["capture_prompt_or_response_content"] = True
    assert analyze_contract(item)["decision"] == "BLOCK"
