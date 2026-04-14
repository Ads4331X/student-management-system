"""
All CSV file read/write operations using pandas.
Implement all data persistence functions.

Uses pandas for clean CSV handling.
All four files: users.csv, passwords.csv, grades.csv, eca.csv
"""

import os
import pandas as pd
from models import User, Student, Admin, SUBJECTS

#  file paths
DATA_DIR = os.path.join(os.path.dirname(_file_), "data")
USERS_CSV     = os.path.join(DATA_DIR, "users.csv")
PASSWORDS_CSV = os.path.join(DATA_DIR, "passwords.csv")
GRADES_CSV    = os.path.join(DATA_DIR, "grades.csv")
ECA_CSV       = os.path.join(DATA_DIR, "eca.csv")



# users
def load_users():
    """
    Load users from users.csv returns in key-value pair {username: user obj}.
    """
    try:
        df = pd.read_csv(USERS_CSV, dtype=str).fillna("") # loads all value as string and replaces missing values with ""
        users = {}
        for _, row in df.iterrows():
            if row["role"] == "admin":
                # create an object user of admin 
                user = Admin(row["user_id"], row["username"], row["full_name"],
                             row["email"], row["phone"], row["address"])
            else:
                # create an object user of student
                user = Student(row["user_id"], row["username"], row["full_name"],
                               row["email"], row["phone"], row["address"])
            users[row["username"]] = user # store user object using username as key
        return users
    
    except FileNotFoundError:
        return {}


def save_users(users):
    """Save a dict of {username: User} back to users.csv."""
    rows = [u.to_dict() for u in users.values()] # stores a list of dictionaries from user objects
    df = pd.DataFrame(rows) # makes stored data into dataframe
    df.to_csv(USERS_CSV, index=False) # save to user.csv file


def get_user_by_id(user_id):
    """Return a User object matching the given user_id, or None."""
    users = load_users() # loads all the user in dict as {username: user obj}
    for user in users.values(): # itterate through each user obj
        if user.user_id == user_id: # check if the user's ID matches the given user_id
            return user
    return None


# passwords
def load_passwords():
    """
    Load passwords from passwords.csv returns in key-value pair {username: pass}.
    """
    try:
        df = pd.read_csv(PASSWORDS_CSV, dtype=str).fillna("") # reads passwords.csv file as strings and empty values are replaced by ""
        return dict(zip(df["username"], df["password"])) # convert username and password columns into a dictionary
    except FileNotFoundError:
        return {}
    

def save_passwords(passwords):
    """Save a dict of {username: password} to passwords.csv."""
    df = pd.DataFrame(list(passwords.items()), columns=["username", "password"])
    df.to_csv(PASSWORDS_CSV, index=False) # save passwords dictionary to CSV file


# grades
def load_grades():
    """
    Load grades.csv as a pandas DataFrame.
    Returns DataFrame with columns: student_id, mathematics, science, english, programming, data_science
    """
    try:
        return pd.read_csv(GRADES_CSV, dtype={"student_id": str}) # reads grades.csv file where student_id is read as string
    except FileNotFoundError:
        # Return an empty DataFrame with the correct columns
        return pd.DataFrame(columns=["student_id"] + SUBJECTS)
    
    def save_grades(df):
    """Save a grades DataFrame to grades.csv."""
    df.to_csv(GRADES_CSV, index=False) 


def get_student_grades(student_id):
    """
    Return a single student's grades as a dict {subject: mark}.
    Returns zeros if student not found.
    """
    df = load_grades() # loads grades dataframe
    row = df[df["student_id"] == student_id] # filter row matching the given student_id
    if row.empty: # not found
        return {s: 0.0 for s in SUBJECTS} # returns 0 grade 
    return row.iloc[0][SUBJECTS].to_dict()


def upsert_student_grades(student_id, marks_dict):
    """
    Insert or update a student's grade row in grades.csv.
    marks_dict: {subject: mark}
    """
    df = load_grades() # loads grades dataframe
    new_row = {"student_id": student_id, **marks_dict} 

    if student_id in df["student_id"].values: #  student_id is found
        # update existing row
        for subject, mark in marks_dict.items():
            df.loc[df["student_id"] == student_id, subject] = mark
    else:
        # append new row
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)

    save_grades(df) # save updated DataFrame back to CSV


# ECA
def load_eca():
    """
    Load eca.csv.
    Returns a dict of {student_id: [activity1, activity2, ...]}
    """
    try:
        df = pd.read_csv(ECA_CSV, dtype=str).fillna("") # reads ecs.csv file as strings and replaces missing data as ""
        eca = {}
        for _, row in df.iterrows():
            activities = [a for a in row["activities"].split(";") if a] # split activities string into a list
            eca[row["student_id"]] = activities # store student_id with list of activities {student_id: [activies]}
        return eca
    except FileNotFoundError:
        return {}


def save_eca(eca_dict):
    """Save a dict of {student_id: [activities]} to eca.csv."""
    rows = [{"student_id": sid, "activities": ";".join(acts)} # convert dictionary into a list of dictionaries for CSV storage
            for sid, acts in eca_dict.items()]
    df = pd.DataFrame(rows) # makes a dataframe 
    df.to_csv(ECA_CSV, index=False) # saves to eca.csv file


def get_student_eca(student_id):
    """Return list of ECA activities for a student."""
    eca = load_eca()  # loads eca dataframe
    return eca.get(student_id, []) 


def upsert_student_eca(student_id, activities):
    """Insert or update ECA activities for a student."""
    eca = load_eca() # loads eca dataframe
    eca[student_id] = activities 
    save_eca(eca) # save to eca.csv file

    
