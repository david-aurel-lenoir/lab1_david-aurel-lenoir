import csv
import sys
import os


def load_csv_data():
    """
    Prompts the user for a filename, checks if it exists,
    and extracts all fields into a list of dictionaries.
    """
    filename = input("Enter the name of the CSV file to process (e.g., grades.csv): ")

    if not os.path.exists(filename):
        print(f"Error: The file '{filename}' was not found.")
        sys.exit(1)

        assignments = []

    try:
        with open(filename, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                assignments.append({
                    'assignment': row['assignment'],
                    'group': row['group'],
                    'score': float(row['score']),
                    'weight': float(row['weight'])
                })
        return assignments
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
        sys.exit(1)


def validate_scores(data):
    """a) Every score must be a percentage between 0 and 100."""
    errors = []
    for row in data:
        if not (0 <= row['score'] <= 100):
            errors.append(f"  - '{row['assignment']}': score {row['score']} is outside 0-100")
    return errors

def validate_weights(data):
    """b) Total weights = 100, Formative = 60, Summative = 40."""
    errors = []
    total = sum(r['weight'] for r in data)
    formative = sum(r['weight'] for r in data if r['group'].strip().lower() == 'formative')
    summative = sum(r['weight'] for r in data if r['group'].strip().lower() == 'summative')

    if round(total, 2) != 100:
        errors.append(f"  - Total weight is {total}, expected 100")
    if round(formative, 2) != 60:
        errors.append(f"  - Formative weight is {formative}, expected 60")
    if round(summative, 2) != 40:
        errors.append(f"  - Summative weight is {summative}, expected 40")

    return errors, total, formative, summative


def calculate_group_contribution(data, group_name):
    """
    Weighted contribution of one group toward the final grade.
    contribution = sum(score/100 * weight)
    """
    return sum((r['score'] / 100) * r['weight']
               for r in data if r['group'].strip().lower() == group_name)


def find_resubmissions(data):
    """
    e) Failed formative assignments (< 50%), keeping only those
    tied at the highest weight.
    """
    failed = [r for r in data
              if r['group'].strip().lower() == 'formative' and r['score'] < 50]
    if not failed:
        return []
    max_weight = max(r['weight'] for r in failed)
    return [r for r in failed if r['weight'] == max_weight]

def evaluate_grades(data):
    """
    Implement your logic here.
    'data' is a list of dictionaries containing the assignment records.
    """
    print("\n--- Processing Grades ---")

    if not data:
        print("Error: No assignment records found. The CSV file appears to be empty.")
        return

    # a) Grade validation
    score_errors = validate_scores(data)
    if score_errors:
        print("\n[FAIL] Grade validation:")
        for e in score_errors:
            print(e)
        sys.exit(1)
    print("[OK] All scores are within 0-100.")

    # b) Weight validation
    weight_errors, total_w, form_w, summ_w = validate_weights(data)
    if weight_errors:
        print("\n[FAIL] Weight validation:")
        for e in weight_errors:
            print(e)
        sys.exit(1)
    print(f"[OK] Weights valid (Total={total_w}, Formative={form_w}, Summative={summ_w}).")

    # c) Final grade and GPA
    formative_total = calculate_group_contribution(data, 'formative')
    summative_total = calculate_group_contribution(data, 'summative')
    final_grade = formative_total + summative_total
    gpa = (final_grade / 100) * 5.0

    # d) Pass/Fail — needs >= 50% of the group's own maximum
    formative_pct = (formative_total / form_w) * 100 if form_w else 0
    summative_pct = (summative_total / summ_w) * 100 if summ_w else 0
    passed = formative_pct >= 50 and summative_pct >= 50

    # Report
    print("\n" + "=" * 55)
    print("             ACADEMIC TRANSCRIPT")
    print("=" * 55)
    print(f"{'Assignment':<35}{'Cat':<6}{'Score':>7}{'Wt':>6}{'Final':>8}")
    print("-" * 62)
    for r in data:
        cat = 'FA' if r['group'].strip().lower() == 'formative' else 'SA'
        contribution = (r['score'] / 100) * r['weight']
        print(f"{r['assignment']:<35}{cat:<6}{r['score']:>7.1f}{r['weight']:>6.1f}{contribution:>8.2f}")
    print("-" * 62)
    print(f"Formatives (60): {formative_total:.2f}  ->  {formative_pct:.2f}%")
    print(f"Summatives (40): {summative_total:.2f}  ->  {summative_pct:.2f}%")
    print(f"Total Grade    : {final_grade:.2f} / 100")
    print(f"GPA            : {gpa:.3f} / 5.0")
    print("=" * 55)

    # f) Final decision
    print(f"Status: {'PASSED' if passed else 'FAILED'}")
    if not passed:
        if formative_pct < 50:
            print("  Reason: Formative average below 50%.")
        if summative_pct < 50:
            print("  Reason: Summative average below 50%.")

    resubs = find_resubmissions(data)
    if resubs:
        names = ", ".join(r['assignment'] for r in resubs)
        print(f"Available for resubmission: {names}")
    else:
        print("Available for resubmission: None")
    print("=" * 55)


if __name__ == "__main__":
    # 1. Load the data
    course_data = load_csv_data()

    # 2. Process the features
    evaluate_grades(course_data)
