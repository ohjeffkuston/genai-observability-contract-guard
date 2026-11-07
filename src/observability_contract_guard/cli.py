from __future__ import annotations

import argparse
import json

from .analyzer import analyze_contract, load_contract


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a GenAI evaluation observability contract")
    parser.add_argument("contract")
    args = parser.parse_args()
    report = analyze_contract(load_contract(args.contract))
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["decision"] == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
