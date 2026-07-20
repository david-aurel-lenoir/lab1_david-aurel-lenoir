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

