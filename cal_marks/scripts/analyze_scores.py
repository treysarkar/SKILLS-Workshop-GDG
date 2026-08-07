#!/usr/bin/env python3

import csv
import json
import sys


def get_grade(score):
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


def read_mark(value):
    """Treat a missing mark as zero."""
    if value.strip() == "":
        return 0.0
    return float(value)


def analyze_results(csv_file):
    students = []

    with open(csv_file, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            quiz_1 = read_mark(row["quiz_1"])
            quiz_2 = read_mark(row["quiz_2"])
            midterm = read_mark(row["midterm"])
            final_exam = read_mark(row["final_exam"])
            attendance = read_mark(row["attendance_pct"])

            # Fixed weights make the calculation deterministic.
            overall = (
                quiz_1 * 0.10
                + quiz_2 * 0.10
                + midterm * 0.30
                + final_exam * 0.50
            )

            overall = round(overall, 2)

            students.append(
                {
                    "student_id": row["student_id"],
                    "name": row["name"],
                    "overall_score": overall,
                    "grade": get_grade(overall),
                    "missing_quiz": (
                        row["quiz_1"].strip() == ""
                        or row["quiz_2"].strip() == ""
                    ),
                    "requires_support": (
                        overall < 50 or attendance < 75
                    ),
                }
            )

    # Keep the output order consistent.
    students.sort(key=lambda student: student["student_id"])

    class_average = round(
        sum(student["overall_score"] for student in students)
        / len(students),
        2,
    )

    return {
        "class_average": class_average,
        "students": students,
    }


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 analyze_scores.py student_results.csv")
        raise SystemExit(1)

    results = analyze_results(sys.argv[1])
    print(json.dumps(results, indent=2, sort_keys=True))