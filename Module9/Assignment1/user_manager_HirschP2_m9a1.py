#!/usr/bin/python3
# HirschP2
# Module 9: Assignment 1 -- Linux User Management
# CIT 383 | Scripting I
# 2025/04/09

import subprocess       # For issuing system commands
import pwd              # For evaluating an accounts creation
import random, string   # For generating random passwords
import crypt
            # For encrypting a password before passing it
import argparse # https://docs.python.org/3/library/argparse.html

# Create the parser to read in command line arguments
parser=argparse.ArgumentParser(
    description='Linux User Account Management Script - Creates, deletes, and modifies system user accounts.',
    epilog='CIT 383 | Scripting I \\\\ Module 9: Assignment 1 -- Linux User Management \\\\ HirschP2@nku.edu')

# Set mutually exclusive group so that only one of the three main operations may be used at once
chosenOperation=parser.add_mutually_exclusive_group(required=True)
chosenOperation.add_argument('--create',action='store_true',help='Create new user')
chosenOperation.add_argument('--delete',action='store_true',help='Delete existing user')
chosenOperation.add_argument('--modify',action='store_true',help='Modify existing user to lock, change full name, or make root')

# Define all other needed flags
parser.add_argument('--username', type=str, help='Username of user')
parser.add_argument('--fullname', type=str, help='Full name of user')
parser.add_argument('--password', type=str, help='Password for user (optional)')
parser.add_argument('--lock', action='store_true', help='Lock user account')
parser.add_argument('--add_root', action='store_true', help='Add user to root group')
args=parser.parse_args()

def create_user(username:str,fullname:str,password:str=None):
    # If no password is provided, generate one randomly
    #   Character space is upper/lowercase letters, numbers, and punctuations
    #   Generate a 12 character long string given the character set
    passPassed=True
    if password is None:
        passPassed=False
        chars=string.ascii_letters+string.digits+string.punctuation
        password=''.join(random.choices(chars,k=12))
        print(f'Generated password for {username}: {password}')
    
    # Encrypt the password
    epassword=crypt.crypt(password)
    
    # Issue the system command to create the new account
    try:
        subprocess.run(['useradd',username,'-c',fullname,'-p',epassword],check=True)
    except Exception as e:
        print(f'ERROR: Unable to create new user:')
        return 1
    
    # If password was script-generated, force a password change on first login
    if not passPassed:
        subprocess.call(['chage','-d','0',username])
    
    print(f"User '{username}' created successfully.")
    return 0


# Given a username, delete that user if it exists.
def delete_user(username:str):
    # Check if the user exists, if not, end the function.
    if not user_exists(username):
        print(f'ERROR: No such user, "{username}"')
        return 1
    
    # Upon verifying a user exists, issue a command to delete user reporting if an error occurs
    try:
        subprocess.run(['userdel',username],check=True)
    except Exception as e:
        print(f'ERROR: Unable to delete user.')
        return 1
    print(f"User '{username}' deleted successfully.")
    return 0


# Given a username, modify the user as desired.
#   lock - If true, locks the user account, defaults to false
#   new_fullname - Takes a string to change user's fullname, if not provided will not change.
#   add_root - If true, adds user to root group, defaults to false
def modify_user(username:str,lock:bool=False,new_fullname:str=None,add_root:bool=False):
    # If the lock field was provided, if so, lock the account
    if lock:
        try:
            subprocess.run(['usermod',username,'-L'],check=True)
            print(f"User '{username}' has been locked.")
        except Exception as e:
            print(f"ERROR: Unable to lock user.")
    
    # If the new_fullname field was provided, if so, change the comment
    if new_fullname is not None:
        try:
            subprocess.run(['usermod',username,'-c',new_fullname],check=True)
            print(f"User '{username}' has been updated to fullname {new_fullname}.")
        except Exception as e:
            print(f"ERROR: Unable to change full name.")
    
    # If the add_root field was provided, if so, add user to root group
    if add_root:
        try:
            subprocess.run(['usermod',username,'-aG','root'],check=True)
            print(f"User '{username}' added to root group.")
        except Exception as e:
            print(f"ERROR: Unable to add user to root group.")


# Given a username, return True if user exists, false if it does not.
def user_exists(username):
    try:
        pwd.getpwnam(username)
        return True
    except KeyError:
        return False


# Ensures required fields are provided and passes off script to the appropriate function.
def main():
    if args.username is None:
        print("--username field is required.")
        exit()
    
    if args.create:
        if args.fullname is None:
            print("--fullname field is required.")
            exit()
        create_user(args.username,args.fullname,args.password)
    
    elif args.delete:
        delete_user(args.username)
    
    elif args.modify:
        modify_user(args.username,lock=args.lock,new_fullname=args.fullname,add_root=args.add_root)

main()