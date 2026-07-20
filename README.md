# Lab 1: Grade Evaluator & Archiver

My individual coding lab for Introduction to Python Programming and Databases.
It has two parts: a Python program that reads a CSV of grades and says if the
student passed, and a Bash script that archives the CSV file.

## Files

- `grade-evaluator.py` - the Python program
- `organizer.sh` - the Bash script

## What you need

Python 3 and a terminal that can run Bash (Linux, or Git Bash / WSL on
Windows). I only used `csv`, `sys` and `os`, which come with Python.

## Making the grades.csv file

`grades.csv` is not in this repository because its in the gitignore. but take note each time to run the `organizer.sh` the grades.csv content is removed. so y'll have to copy it back inside

grades.csv

It has to look like this:
assignment,group,score,weight
Quiz,Formative,85,20
Group Exercise,Formative,40,20
Functions and Debugging Lab,Formative,45,20
Midterm Project - Simple Calculator,Summative,70,20
Final Project - Text-Based Game,Summative,60,20

The weights must add up to 100, with 60 for Formative and 40 for Summative.

## Running the Python program

```bash
python3 grade-evaluator.py
```

It asks for a file name. Type `grades.csv` and press Enter. On Windows, try
`python` if `python3` doesn't work.

The program checks that the scores are between 0 and 100 and that the weights
are correct, then calculates the final grade and the GPA with
`GPA = (Total Grade / 100) * 5.0`. To pass, the student needs at least 50% in
the Formative group AND at least 50% in the Summative group, not just 50%
overall. It also shows the failed Formative assignment with the biggest weight
so it can be resubmitted, or both of them if there is a tie.

If the file is missing, empty, or has wrong scores or weights, it prints an
error and stops.

## Running the Bash script

```bash
chmod +x organizer.sh
./organizer.sh
```

You only need `chmod` once. If you get a permission error, use
`bash organizer.sh` instead.

The script creates an `archive` folder if there isn't one, makes a timestamp,
moves `grades.csv` into the folder as `grades_TIMESTAMP.csv`, creates a new
empty `grades.csv`, and adds a line to `organizer.log`. The log keeps every run.

It prints something like:
archive folder not found, creating it
timestamp is 20260720-143052
moved grades.csv to archive/grades_20260720-143052.csv
created a new empty grades.csv
log updated

You can check with `ls archive/` and `cat organizer.log`.

## Everything together

```bash
cp grades.sample.csv grades.csv
python3 grade-evaluator.py
./organizer.sh
cat organizer.log
```

After running `organizer.sh` the CSV is empty, so copy the sample back before
running the Python program again.
