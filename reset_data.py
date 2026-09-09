"""Reset stored face/label data used by the face-recognition scripts.

This script deletes the persisted model data files in `data/` so the project starts
with a clean slate.

Usage:
    python reset_data.py

Optional:
    python reset_data.py --attendance  # also deletes generated attendance CSV files
"""

import argparse
import glob
import os
from pathlib import Path


def remove_file(path: Path) -> bool:
    if path.exists():
        path.unlink()
        return True
    return False


def main() -> None:
    parser = argparse.ArgumentParser(description="Delete saved face/name data (and optionally attendance records).")
    parser.add_argument(
        "--attendance",
        action="store_true",
        help="Also delete attendance CSV files in the Attendance/ folder.",
    )
    args = parser.parse_args()

    data_dir = Path("data")
    targets = [data_dir / "names.pkl", data_dir / "faces_data.pkl", data_dir / "faces.pkl"]

    removed = []
    for t in targets:
        if remove_file(t):
            removed.append(str(t))

    if args.attendance:
        att_dir = Path("Attendance")
        for csv_path in att_dir.glob("*.csv"):
            if remove_file(csv_path):
                removed.append(str(csv_path))

    if removed:
        print("Removed:")
        for p in removed:
            print("  -", p)
    else:
        print("No face/name data files were found to remove.")


if __name__ == "__main__":
    main()
