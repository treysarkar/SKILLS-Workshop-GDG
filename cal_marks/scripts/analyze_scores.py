
import argparse
import csv
import json
import sys
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

WEIGHTS = {
    "quiz": Decimal("0.20"),
    "midterm": Decimal("0.30"),
    "final": Decimal("0.50"),
}

REQUIRED_COLUMNS = {"student_id", "name", *WEIGHTS}


def round_two(value: Decimal) -> Decimal:
    return value.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def grade_for(score: Decimal) -> str:
    if score >= 90:
        return "A"
    if score >= 80:
        return "B"
    if score >= 70:
        return "C"
    if score >= 60:
        return "D"
    if score >= 50:
        return "E"
    return "F"


def parse_mark(row: dict[str, str], field: str, row_number: int) -> Decimal:
    try:
        mark = Decimal(row[field])
    except Exception as exc:
        raise ValueError(
            f"Row {row_number}: {field} must be a number."
        ) from exc

    if not Decimal("0") <= mark <= Decimal("100"):
        raise ValueError(
            f"Row {row_number}: {field} must be between 0 and 100."
        )

    return mark


def analyze(csv_path: Path) -> dict:
    with csv_path.open(newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        columns = set(reader.fieldnames or [])
        missing = REQUIRED_COLUMNS - columns

        if missing:
            raise ValueError(
                "Missing required columns: " + ", ".join(sorted(missing))
            )

        students = []

        for row_number, row in enumerate(reader, start=2):
            marks = {
                field: parse_mark(row, field, row_number)
                for field in WEIGHTS
            }

            total = round_two(
                sum(marks[field] * WEIGHTS[field] for field in WEIGHTS)
            )

            students.append(
                {
                    "student_id": row["student_id"].strip(),
                    "name": row["name"].strip(),
                    "weighted_total": float(total),
                    "grade": grade_for(total),
                    "requires_support": total < Decimal("50"),
                }
            )

    if not students:
        raise ValueError("The CSV contains no student records.")

    # Stable ordering makes repeated runs produce identical output.
    students.sort(key=lambda item: item["student_id"])

    scores = [Decimal(str(item["weighted_total"])) for item in students]
    average = round_two(sum(scores) / Decimal(len(scores)))

    grade_distribution = {
        grade: sum(student["grade"] == grade for student in students)
        for grade in ["A", "B", "C", "D", "E", "F"]
    }

    return {
        "student_count": len(students),
        "class_average": float(average),
        "highest_score": float(max(scores)),
        "lowest_score": float(min(scores)),
        "grade_distribution": grade_distribution,
        "students": students,
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Calculate deterministic weighted student results."
    )
    parser.add_argument("csv_file", type=Path)
    args = parser.parse_args()

    try:
        result = analyze(args.csv_file)
    except (OSError, ValueError) as exc:
        print(json.dumps({"error": str(exc)}), file=sys.stderr)
        return 1

    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())