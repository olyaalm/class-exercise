import argparse
import csv
import logging
import sys
from pathlib import Path


def check_data(filename):
    """Read the CSV file and check for missing values."""
    with open(filename, "r", newline="") as f:
        reader = csv.reader(f)
        rows = list(reader)

    if not rows:
        raise ValueError(f"CSV file '{filename}' is empty.")

    header = rows[0]
    data = rows[1:]
    missing_rows = []

    for row_number, row in enumerate(data, start=2):
        if any(value.strip() == "" for value in row):
            missing_rows.append(row_number)

    return header, data, missing_rows


def main():
    parser = argparse.ArgumentParser(
        description="Check the quality of a CSV file"
    )
    parser.add_argument(
        "--input",
        "-i",
        required=True,
        help="CSV file to check",
    )
    parser.add_argument(
        "--output",
        "-o",
        default="data_quality.txt",
        help="Output report filename",
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Show detailed DEBUG messages",
    )
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(levelname)s: %(message)s",
    )

    input_path = Path(args.input)
    if not input_path.is_file():
        print(f"File not found: '{args.input}'")
        sys.exit(1)

    logging.info("File validated: '%s'", args.input)
    logging.debug("Checking data for missing values...")

    header, data, missing_rows = check_data(args.input)

    report_path = Path(args.output)
    with report_path.open("w", newline="") as f:
        f.write(f"Number of rows: {len(data)}\n")
        f.write(f"Number of columns: {len(header)}\n")
        f.write(f"Number of rows with missing values: {len(missing_rows)}\n")

    if args.verbose:
        logging.debug("Missing rows: %s", missing_rows)

    print(f"Report saved to: '{args.output}'")


if __name__ == "__main__":
    main()
