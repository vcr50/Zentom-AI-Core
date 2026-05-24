import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_DATASET_PATH = PROJECT_ROOT / "datasets" / "zentom" / "zentom_alpaca_v0_1.json"

MIN_USEFUL_EXAMPLES = 100
MIN_FIELD_CHARS = {
    "instruction": 40,
    "input": 40,
    "output": 40,
}
SAFETY_TERMS = ("policy", "risk", "approval", "runbook", "safety")


def load_dataset(path: Path) -> list[dict[str, Any]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise ValueError("Dataset root must be a JSON array.")

    invalid_rows = [
        index
        for index, record in enumerate(data, start=1)
        if not isinstance(record, dict)
    ]
    if invalid_rows:
        raise ValueError(f"Dataset rows must be objects. Invalid rows: {invalid_rows}")

    return data


def parse_output(record: dict[str, Any]) -> tuple[dict[str, Any] | None, str | None]:
    output = record.get("output")

    if isinstance(output, dict):
        return output, None

    if not isinstance(output, str) or not output.strip():
        return None, "output is missing or not a string"

    try:
        parsed = json.loads(output)
    except json.JSONDecodeError as exc:
        return None, f"output is not valid JSON: {exc.msg}"

    if not isinstance(parsed, dict):
        return None, "output JSON must be an object"

    return parsed, None


def normalize_record(record: dict[str, Any]) -> str:
    return json.dumps(
        {
            "instruction": str(record.get("instruction", "")).strip(),
            "input": str(record.get("input", "")).strip(),
            "output": str(record.get("output", "")).strip(),
        },
        sort_keys=True,
        separators=(",", ":"),
    )


def check_dataset(dataset: list[dict[str, Any]]) -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []

    if len(dataset) < MIN_USEFUL_EXAMPLES:
        warnings.append(
            f"Dataset has {len(dataset)} examples; target at least {MIN_USEFUL_EXAMPLES} for a basic experiment."
        )

    fingerprints = [normalize_record(record) for record in dataset]
    duplicate_counts = {
        fingerprint: count
        for fingerprint, count in Counter(fingerprints).items()
        if count > 1
    }
    duplicate_total = sum(count - 1 for count in duplicate_counts.values())
    if duplicate_total:
        errors.append(f"Found {duplicate_total} duplicate example(s).")

    for index, record in enumerate(dataset, start=1):
        for field in ("instruction", "input", "output"):
            value = record.get(field)
            if not isinstance(value, str) or not value.strip():
                errors.append(f"Row {index}: missing {field}.")
                continue

            if len(value.strip()) < MIN_FIELD_CHARS[field]:
                warnings.append(f"Row {index}: {field} looks too short.")

        instruction = str(record.get("instruction", ""))
        lower_instruction = instruction.lower()
        missing_safety_terms = [
            term
            for term in SAFETY_TERMS
            if term not in lower_instruction
        ]
        if missing_safety_terms:
            errors.append(
                f"Row {index}: safety instruction missing term(s): {', '.join(missing_safety_terms)}."
            )

        output_json, output_error = parse_output(record)
        if output_error:
            errors.append(f"Row {index}: {output_error}.")
            continue

        if "runbookKey" not in output_json:
            errors.append(f"Row {index}: output missing runbookKey.")

        if "confidenceScore" not in output_json:
            errors.append(f"Row {index}: output missing confidenceScore.")

    return {
        "datasetCount": len(dataset),
        "duplicateExamples": duplicate_total,
        "errors": errors,
        "warnings": warnings,
        "passed": not errors,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Check Zentom Alpaca dataset quality.")
    parser.add_argument(
        "dataset_path",
        nargs="?",
        default=str(DEFAULT_DATASET_PATH),
        help="Path to a Zentom Alpaca JSON dataset.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Print machine-readable JSON output.",
    )
    args = parser.parse_args()

    path = Path(args.dataset_path)

    try:
        dataset = load_dataset(path)
        result = check_dataset(dataset)
    except Exception as exc:
        result = {
            "datasetCount": 0,
            "duplicateExamples": 0,
            "errors": [str(exc)],
            "warnings": [],
            "passed": False,
        }

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"Dataset: {path}")
        print(f"Count: {result['datasetCount']}")
        print(f"Duplicate examples: {result['duplicateExamples']}")
        print(f"Passed: {result['passed']}")

        if result["warnings"]:
            print("\nWarnings:")
            for warning in result["warnings"]:
                print(f"- {warning}")

        if result["errors"]:
            print("\nErrors:")
            for error in result["errors"]:
                print(f"- {error}")

    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
