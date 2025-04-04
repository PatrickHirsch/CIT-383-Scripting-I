#!/usr/bin/python3
# HirschP2
# Module 7: Assignment 1 -- File and Directory Management
# CIT 383 | Scripting I
# 2025/03/31

import os
import subprocess
import shutil
import zipfile
import datetime 
import dateutil.relativedelta

VALID_ARCHIVE_TYPES=["zip","gztar","tar","bztar","xztar"]

# Given a path, check if a directory exists there by returning a response code.
#   -1  - A FILE currently exists at path
#   0   - Nothing exists at path currently
#   1   - A directory DOES currently exist at path
def checkDirectoryExists(dir_path: str):
    if(os.path.exists(dir_path)==False):
        return 0
    if(os.path.isdir(dir_path)):
        return 1
    if(os.path.isfile(dir_path)):
        return -1

# Given two directory paths, create a copy of the first inside the second
#   If either path does not exist function terminates with an error
#   Directory is copied with an invocation of a simple `cp` bash command.
def back_up_dir(dir_path:str,dest_path:str):
    # Ensure both directories passed exist and are directories rather than files
    if(checkDirectoryExists(dir_path)<1 or checkDirectoryExists(dest_path)<1):
        raise NameError("Provided file path either does not exist, or is a file.")
    
    # Invoke a simple rsync command to copy dir_path to dest_path 
    #   handles any errors just by reporting an error occurred and the error message given
    try:
        subprocess.run(['rsync','-a',dir_path,dest_path],check=True)
    except Exception as e:
        print(f"An unknown error occurred in backing up your directory: {e}")
    

# Given a directory path, archive type, and file name create an archive in user's home directory
def archive_dir(dir_name: str, arch_type: str, archive_base_name: str):
    # Ensure the directory to be archived exists and is a directory, raise error if not.
    if(checkDirectoryExists(dir_name)<1):
        raise NameError("Provided file path either does not exist, or is a file.")
    
    # Ensure the given archive type is supported, raise error if not.
    if arch_type not in VALID_ARCHIVE_TYPES:
        raise TypeError(f"Unsupported archive type: {arch_type}.")
    
    # Handle file paths as needed for shutil.make_archive()
    archive_base_name=os.path.expanduser(f"~/{archive_base_name}")
    dir_name=os.path.abspath(dir_name)
    root_dir=os.path.dirname(dir_name)
    base_dir=os.path.basename(dir_name)
    
    ret=shutil.make_archive(archive_base_name,arch_type,root_dir=root_dir,base_dir=base_dir)
    print(f"Created {arch_type} archive at {ret}.")
    

# Given a file path to a ZIP and a file size threshold in KB report on all files within zip above threshold
def get_large_archive(zip_file_path:str,threshold:int):
    # Handle exceptions incase file path given is not valid.
    if(checkDirectoryExists(zip_file_path)>-1):
        raise NameError("Provided file path either does not exist, or is a directory.")
    if not zipfile.is_zipfile(zip_file_path):
        raise TypeError("Provided file path is not a zip file.")
    
    # Confirming this is indeed a zip, print a header before processing it:
    print(f"Analyzing ZIP file, {zip_file_path}...\n\nFiles larger than {threshold}KB:")
    
    # Convert threshold from KB to Bytes
    threshold=threshold*1024
    
    # Iterate through each file in the ZIP, reporting on each over the threshold.
    #   Prints each large file's name, OS, and excesses file size
    with zipfile.ZipFile(zip_file_path) as zip:
        for info in zip.infolist():
            if info.file_size>threshold:
                if info.create_system==0:
                    OS="Windows"
                elif info.create_system==3:
                    OS="Unix"
                else:
                    OS="UNKNOWN"
                print(f" -{info.filename} created on {OS} exceeds threshold by {(info.file_size-threshold)/1024:.2f}KB")


# Given a directory, list all files within modified within the the last month via a `find` bash command
def get_recently_modified_files(dir_path:str):
    # Ensure the directory given exists.  
    #   If it does not, or is a file, default to current working directory.
    if(checkDirectoryExists(dir_path)<1):
        dir_path="."
    
    # Get the timestamp for one month ago, i.e. the lower bounds for the search
    #   https://stackoverflow.com/questions/9724906/python-date-of-the-previous-month
    monthAgo=datetime.datetime.now()+dateutil.relativedelta.relativedelta(months=-1)
    
    # Print a header with directory being searched and lower bounds for search
    print(f"files modified since {monthAgo.strftime('%B %d, %Y')} in {dir_path}:")
    
    # Issue a `find` command to list for files in dir_path modified since monthAgo
    out=subprocess.run(['find',dir_path,'-type','f','-newermt',monthAgo.strftime("%Y%m%d")],check=True)
    

# Series of "Invoke" functions to act as drivers for individual operations a user may select,
#   Prompts for necessary input from user and passes them onto the appropriate functions
def invoke_Backup():
    print("# Create backup of directory")
    dir_path=input("Provide path of directory to be backed up: ")
    dest_path=input("Provide path to backup to: ")
    try:
        back_up_dir(dir_path,dest_path)
    except Exception as e:
        print(f'ERROR: {e}')
def invoke_Archive():
    print("# Create archive of directory")
    dir_name=input("Provide path of directory to be archived: ")
    arch_type=input(f"Provide archive type to be created ({'/'.join(VALID_ARCHIVE_TYPES)}): ")
    archive_base_name=input("Provide filename of archive to be created: ")
    try:
        archive_dir(dir_name,arch_type,archive_base_name)
    except Exception as e:
        print(f'ERROR: {e}')
def invoke_Large():
    print("# Analyze .zip for large files")
    zip_file_path=input("Provide path to .zip file to analyze: ")
    threshold=input("Provide minimum file size threshold to be reported: ")
    try:
        get_large_archive(zip_file_path,int(threshold))
    except Exception as e:
        print(f'ERROR: {e}')
def invoke_Recent():
    print("# List files of in directory modified within last month: ")
    dir_path=input("Provide path to directory to analyze: ")
    try:
        get_recently_modified_files(dir_path)
    except Exception as e:
        print(f'ERROR: {e}')


# Primary driver of the program, prompts user with a menu then takes an int as input
#   Passes off user to necessary "invoke" function based on int provided.
def main():
    print("""Select your operation:
1. Create backup of directory.
2. Create archive of directory.
3. Analyzing .zip archive for large files
4. List recently modified files in directory.""")
    userChoice=input(":")
    
    try:
        userChoice=int(userChoice)
    except Exception as e:
        userChoice=-1
    print("\n\n")
    
    if userChoice==1:
        invoke_Backup()
    elif userChoice==2:
        invoke_Archive()
    elif userChoice==3:
        invoke_Large()
    elif userChoice==4:
        invoke_Recent()
    else:
        print("Invalid selection.")
    print("\n\n")
    
while True:
    main()
