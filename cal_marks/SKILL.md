---
name: cal_marks
description: Analyze student assessment CSV files using fixed grading rules and produce accurate summaries. Use when asked to calculate weighted results, assign grades, identify students needing academic support, or summarize class performance.
---

# Analyze Student Results

Use the bundled Python script for all calculations. Do not calculate
weighted scores or grades manually.

## Workflow

1. Confirm that the input is a CSV file containing:
  'student_id','name','quiz_1','quiz_2','midterm','final_exam','attendance_pct'
2. Run:

   `python3 scripts/analyze_scores.py <input.csv>`

3. Read the JSON returned by the script.
4. Report:
   - class average;
   - highest and lowest score;
   - grade distribution;
   - students requiring support.

   in a table
5. Explain the findings in clear, supportive language.
6. Never invent missing marks or student information.

Treat a student as requiring support when the weighted total is below 50.