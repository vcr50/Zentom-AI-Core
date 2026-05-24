import argparse
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[3]
API_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(API_ROOT))

from app.database import SessionLocal, init_database  # noqa: E402
from app.services.dataset_service import export_dataset, save_dataset_json  # noqa: E402


DEFAULT_OUTPUT = PROJECT_ROOT / "datasets" / "zentom" / "zentom_alpaca_v0_1.json"


def main() -> None:
    parser = argparse.ArgumentParser(description="Export Zentom memories as an Alpaca dataset.")
    parser.add_argument(
        "--output",
        default=str(DEFAULT_OUTPUT),
        help="Path for the exported JSON file.",
    )
    args = parser.parse_args()

    init_database()
    db = SessionLocal()
    try:
        dataset = export_dataset(db, format="alpaca")
        path = save_dataset_json(dataset, args.output)
    finally:
        db.close()

    print(f"Exported {len(dataset)} records to {path}")


if __name__ == "__main__":
    main()
