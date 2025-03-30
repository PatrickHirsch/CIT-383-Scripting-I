#!/usr/bin/python3
# HirschP2
# Module 7: Assignment 1 -- File and Directory Management
# CIT 383 | Scripting I
# 2025/03/27

import os
import re

VALID_EXTENTIONS=['txt','png','doc','dat']

# Given a filename prefix and number of files to create, create a specified number of files numbered with a given prefix if they don't already exist.
#   File extension defaults to first listed valid extension
def create_files(file_name_prefix: str, num_of_files: int):
    if num_of_files < 0:
        raise IndexError("num_of_files must be non-negative")
    if isInvalidFilename(file_name_prefix):
        raise TypeError("file_name_prefix deemed invalid filename")
    
    for i in range(num_of_files):
        filename=file_name_prefix+str(i)+'.'+VALID_EXTENTIONS[0]
        if(os.path.exists(filename)):
            print(f"Skipped creating file {filename}: already exists.")
        else:
            print(f"Creating file {filename}.")
            open(filename,'a').close()

# Given a directory name, create a new directory with that name if it does not already exist.
def create_dir(name_of_directory: str):
    print(f"Making Directory {name_of_directory}...")
    
    name_of_directory=os.path.expanduser(name_of_directory)
    
    if(os.path.exists(name_of_directory)):
        if(os.path.isdir(name_of_directory)):
            print("Could not create directory, directory already exists with that name.")
        elif(os.path.isfile(name_of_directory)):
            print("Could not create directory, file already exists with that name.")
        return -1
    os.mkdir(name_of_directory)


# Given a filename and a new filename, renames a file assuming new name is no already taken.
def rename_file(filename: str, new_name: str):
    if(os.path.exists(filename)==False):
        raise FileNotFoundError(f"{filename} does not exist.")
        
    if(os.path.exists(new_name)):
        print(f"{new_name} already exists.  {filename} not renamed.")
        return
    
    print(f"Renaming {filename} to {new_name}")
    os.rename(filename,new_name)

# Equivalent to ls command, given a directory path, print the path and the iterate over each file
#   For each file, accordingly print whether its a file or directory, then its name.
def display_contents(directory_name: str):
    print(f"Files in {directory_name}:")
    files=os.listdir(directory_name)
    for file in files:
        if(os.path.isdir(directory_name+"/"+file)):
            file="[D] "+file
        else:
            file="[F] "+file
        print(file)

# Iterates through a directory and changes all files of a specified extension to a different extension
def rename_files_in_directory(target_directory: str, current_ext: str, new_ext: str):
    files=os.listdir(target_directory)
    for file in files:
        newname=re.sub("\."+current_ext+"$","."+new_ext,file)
        if newname != file:
            rename_file(target_directory+'/'+file,target_directory+'/'+newname)

def isInvalidFilename(filename:str)
    return False


def main():
    # Start by printing the current working directory
    print("Current Working Directory:")
    print(os.path.basename(os.getcwd())+" ("+os.getcwd()+")\n")
    
    # Get the new directory to create for the script's execution, deriving username from home directory name.
    newdir=os.path.expanduser('~/CITFall2023'+os.path.basename(os.path.expanduser('~')))
    create_dir(newdir)
    
    # Prompt user for number of files to create, terminating program if an invalid number is given
    numFiles=input("Number of files to create: ")
    try:
        numFiles=int(numFiles)
    except ValueError:
        print(f"{numFiles} not a valid int.  Terminating program.")
        return
    
    # Prompt for filename prefix and call create_files() to handle file creation, 
    #   Handles errors thrown by create_files() by terminating the program with error message,
    filenamePrefix=input("Filename prefix: ")
    try:
        create_files(newdir+'/'+filenamePrefix,int(numFiles))
    except IndexError:
        print(f"{numFiles} is negitive, number of files must be non-negative.  Terminating program.")
        return
    except TypeError:
        print(f".  Terminating program.")
        return
    
    # Prompt the user for a new extension and call rename_files_in_directory() to change extensions
    fileExtention=input("File extension: ")
    if fileExtention not in VALID_EXTENTIONS:
        print(f'{fileExtention} is not a supported file extention.  Valid extentions are {VALID_EXTENTIONS}.  Terminating program.')
        return
    else:
        rename_files_in_directory(newdir,VALID_EXTENTIONS[0],fileExtention)
    
    # Print the contents of the created directory
    display_contents(newdir)
main()


