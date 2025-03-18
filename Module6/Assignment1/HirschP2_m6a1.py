#!/usr/bin/python3
# HirschP2
# Module 6: Assignment 1 -- Reading and Writing Text Files
# CIT 383 | Scripting I
# 2025/03/17

import csv

# Configurable values
MIN_ACCESSIBLE_ATTEMPTS=99
FILENAME_INPUT='employee_logins.csv'
FILENAME_OUTPUT='HirschP2_affected_users.csv'
CSV_HEADERS=['firstname','lastname','login_count']

# Read the specified input file and return an array of dictionaries
def read_user_data():
    ret=[]
    with open(FILENAME_INPUT,mode='r') as file:
        CSVReader=csv.DictReader(file)
        for i in CSVReader:
            ret.append(i)
    return ret

# Given an array of dictionaries supplied by read_user_data(), interpret it handling data accordingly:
#   For each row, if the login attempts exceed the acceptable threshold print name and copy to output file.
#   Returns the number of suspicious attempts
def write_suspicious_logins_data(userData):
    ret=0
    with open(FILENAME_OUTPUT,'w',newline='') as file:
        
        # Check the headers to ensure input file matches expected specification, 
        #   throw an error if headers don't match, otherwise write them to output file
        headers=userData[0].keys()
        if list(headers)!=CSV_HEADERS:
            raise NameError("Headers not as expected.")
        CSVWriter=csv.DictWriter(file,fieldnames=headers)
        CSVWriter.writeheader()
        
        # Iterate through each row of input data and determine if login_count exceeds MIN_ACCESSIBLE_ATTEMPTS
        #   Where true, write to output file, print name, and increment count
        for i in userData:
            if int(i[CSV_HEADERS[2]])>MIN_ACCESSIBLE_ATTEMPTS:
                CSVWriter.writerow(i)
                print(f"Suspicious logins from: {i[CSV_HEADERS[0]]} {i[CSV_HEADERS[1]]}")
                ret+=1
    return ret


def main_HirschP2():
    # Run read_user_data() to read input file.
    #   Exits gracefully w/ error message if file cannot be read.
    try:
        userData=read_user_data()
    except FileNotFoundError:
        print(f'ERROR: Input file, {FILENAME_INPUT}, not found.')
        exit()
    except PermissionError:
        print(f'ERROR: Input file, {FILENAME_INPUT}, could not be read.')
        exit()
    
    # Run write_suspicious_logins_data() to process data.
    #   Exits gracefully w/ error message if output file cannot be written to or data is not as expected.
    try:
        count=write_suspicious_logins_data(userData)
    except PermissionError:
        print(f'ERROR: Could not write to output file, {FILENAME_INPUT}.')
        exit()
    except NameError:
        print(f'ERROR: Input data formated incorrectly, {FILENAME_INPUT}.')
        exit()
    
    print(f'\n{count} total employees with suspicious login attempts.')


main_HirschP2()
