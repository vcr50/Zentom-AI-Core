import argparse
import json
import sys
from pathlib import Path
from typing import Any


EXPERIMENT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = EXPERIMENT_DIR.parents[1]
DEFAULT_DATASET_PATH = PROJECT_ROOT / "datasets" / "zentom" / "zentom_alpaca_v0_1.json"
DEFAULT_OUTPUT_DIR = EXPERIMENT_DIR / "outputs" / "zentom-lora-dry-run"

MIN_EXAMPLES_TO_TRAIN = 100

sys.path.insert(0, str(EXPERIMENT_DIR))

from dataset_quality_check import check_dataset, load_dataset  # noqa: E402


def build_experiment_plan(dataset_path: Path, output_dir: Path, dataset_count: int) -> dict[str, Any]:
    return {
        "status": "experimental",
        "productionModelReplacement": False,
        "datasetPath": str(dataset_path),
        "datasetCount": dataset_count,
        "outputDir": str(output_dir),
        "futureStack": [
            "Unsloth",
            "Hugging Face transformers",
            "Hugging Face datasets",
            "PEFT",
            "TRL",
        ],
        "candidateBaseModels": [
            "Small instruct model for local LoRA/QLoRA validation",
            "Do not use production Zentom model",
        ],
        "safetyRules": [
            "No production model replacement",
            "No secrets, credentials, tokens, personal data, or proprietary payloads",
            "Preserve policy, risk, approval, and runbook safety controls",
            "Fine-tuned output remains recommendation-only",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Prepare a local Zentom LoRA/QLoRA fine-tuning experiment."
    )
    parser.add_argument(
        "--dataset",
        default=str(DEFAULT_DATASET_PATH),
        help="Path to the Alpaca JSON dataset.",
    )
    parser.add_argument(
        "--output-dir",
        default=str(DEFAULT_OUTPUT_DIR),
        help="Directory for future experiment outputs.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Validate and print the experiment plan without training.",
    )
    parser.add_argument(
        "--allow-small-dataset",
        action="store_true",
        help="Allow pipeline-only experiments with fewer than 100 examples.",
    )
    parser.add_argument(
        "--start-training",
        action="store_true",
        help="Reserved for a future implementation. This script does not train yet.",
    )
    args = parser.parse_args()

    dataset_path = Path(args.dataset)
    output_dir = Path(args.output_dir)

    dataset = load_dataset(dataset_path)
    quality = check_dataset(dataset)
    plan = build_experiment_plan(dataset_path, output_dir, quality["datasetCount"])

    print(json.dumps({"quality": quality, "plan": plan}, indent=2))

    if quality["errors"]:
        print("Dataset quality errors must be fixed before any training experiment.", file=sys.stderr)
        return 1

    if quality["datasetCount"] < MIN_EXAMPLES_TO_TRAIN and not args.allow_small_dataset:
        print(
            "Dataset is too small for training. Use --allow-small-dataset only for pipeline validation.",
            file=sys.stderr,
        )
        return 1

    if args.start_training:
        print(
            "Training is intentionally not implemented yet. Add Unsloth/PEFT in a future milestone.",
            file=sys.stderr,
        )
        return 1

    if args.dry_run:
        print("Dry run complete. No model was trained or replaced.")
        return 0

    print("No training started. Use --dry-run for validation.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
