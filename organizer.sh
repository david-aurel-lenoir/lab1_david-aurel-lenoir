#!/bin/bash
# organizer.sh
# This script archives my grades.csv file

# check if the archive folder exists
if [ -d "archive" ]
then
    echo "archive folder already exists"
else
    echo "archive folder not found, creating it"
    mkdir archive
fi

# get the current date and time
timestamp=$(date +%Y%m%d-%H%M%S)
echo "timestamp is $timestamp"

# check if grades.csv is there
if [ ! -f "grades.csv" ]
then
    echo "grades.csv not found!"
    exit 1
fi

# make the new name and move the file
newname="grades_$timestamp.csv"
mv grades.csv archive/$newname
echo "moved grades.csv to archive/$newname"

# create a new empty grades.csv
touch grades.csv
echo "created a new empty grades.csv"

# write to the log file
echo "$timestamp - grades.csv archived as $newname" >> organizer.log
echo "log updated"
