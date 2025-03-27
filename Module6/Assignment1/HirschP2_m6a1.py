#!/usr/bin/python3
# HirschP2
# Module 6: Assignment 1 -- Reading and Writing Text Files
# CIT 383 | Scripting I
# 2025/03/17 - Revised: 2025/03/27

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
#   For each row, if the login attempts exceed the acceptable threshold write appropriate data to list to return.
#   returns list and writes to output file
def write_suspicious_logins_data(userData):
    sus=[['name','login_count','login_count_excess']]
    with open(FILENAME_OUTPUT,'w',newline='') as file:
        
        # Check the headers to ensure input file matches expected specification, 
        #   throw an error if headers don't match, otherwise write them to output file
        headers=userData[0].keys()
        if list(headers)!=CSV_HEADERS:
            raise NameError("Headers not as expected.")
        CSVWriter=csv.writer(file)
        
        # Iterate through each row of input data and determine if login_count exceeds MIN_ACCESSIBLE_ATTEMPTS
        #   Where true, write to output file, print name, and increment count
        for i in userData:
            if int(i[CSV_HEADERS[2]])>MIN_ACCESSIBLE_ATTEMPTS:
                sus.append([i[CSV_HEADERS[1]]+'; '+i[CSV_HEADERS[0]], i[CSV_HEADERS[2]], int(i[CSV_HEADERS[2]])-100])
                
        CSVWriter.writerows(sus)
    return sus

# Given a 2D array, print as a table with column widths suited to expected output of write_suspicious_logins_data()
def printTable(list2D):
    for row in list2D:
        print(f"{row[0]:20s}\t {row[1]:10s}\t {str(row[2]):10s}\t ")

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
        suspicious=write_suspicious_logins_data(userData)
    except PermissionError:
        print(f'ERROR: Could not write to output file, {FILENAME_INPUT}.')
        exit()
    except NameError:
        print(f'ERROR: Input data formated incorrectly, {FILENAME_INPUT}.')
        exit()
    
    printTable(suspicious)
    print(f'\n{len(suspicious)-1} total employees with suspicious login attempts.')


main_HirschP2()
