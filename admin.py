"""
Admin panel: manage users, grades, ECA, and view insights
Implement all admin operations

Uses pandas for grade insights and numpy for basic statistics
"""

import numpy as np
import pandas as pd

import file_handler as fh
from auth import AuthSystem
from models import SUBJECTS
from utils import clear_screen, banner, section, ok, err, info


class AdminPanel:
    """All admin operations: CRUD on students, grades, ECA, and insights."""

    def __init__(self, user):
        self.user = user
        self.auth = AuthSystem()

    # Add New Student 
    def add_student(self):
        """Prompt admin to enter details and register a new student."""
        clear_screen(); banner(); section("ADD NEW STUDENT") # clears screen , displays banner and shows selection of add new student

        try:
            # collect student details from admin
            user_id  = input("  Student ID (e.g. S004): ").strip().upper()
            username = input("  Username              : ").strip().lower()
            name     = input("  Full Name             : ").strip()
            email    = input("  Email                 : ").strip()
            phone    = input("  Phone                 : ").strip()
            address  = input("  Address               : ").strip()
            password = input("  Password              : ").strip()

            if not all([user_id, username, name, email, password]):
                err("  All fields except phone/address are required.")
            else:
                success, msg = self.auth.register_student(
                    user_id, username, name, email, phone, address, password
                )
                ok(f"  {msg}") if success else err(f"  {msg}")

        except Exception as e:
            err(f"  Error: {e}")

        input("\n  Press Enter to continue...")

    #  view all students 
    def view_all_students(self):
        """Display a table of all registered students."""
        clear_screen(); banner(); section("ALL STUDENTS") # clear screen, show banner and section header

        try:
            users = fh.load_users() # loads all users {username: user obj}
            students = [u for u in users.values() if u.role == "student"]

            if not students:
                info("  No students found.") 
            else:
                print(f"\n  {'ID':<8} {'Username':<12} {'Full Name':<22} {'Email'}") 
                print("  " + "─" * 65)
                for s in sorted(students, key=lambda u: u.user_id): # sort by user id
                    print(f"  {s.user_id:<8} {s.username:<12} {s.full_name:<22} {s.email}")
                print(f"\n  Total: {len(students)} student(s)")

        except Exception as e:
            err(f"  Error: {e}")

        input("\n  Press Enter to continue...")

    # update student profile
    def update_student(self):
        """Update personal information for a student by ID."""
        clear_screen(); banner(); section("UPDATE STUDENT PROFILE") # clear screen, show banner and section header

        try:
            # ask to admin enter student_id
            uid = input("  Enter Student ID: ").strip().upper()
            users = fh.load_users()# loads all users {username: user obj}

            # find the student
            target = None
            for u in users.values(): # itterate through users
                if u.user_id == uid and u.role == "student": # finds student by student_id
                    target = u
                    break 
            if not target: # not found
                err(f"  Student '{uid}' not found.")
                input("\n  Press Enter to continue...")
                return

            target.display() 
            print("\n  (Press Enter to keep current value)\n")

            # ask admin for new details
            new_name    = input(f"  Full Name  [{target.full_name}]: ").strip()
            new_email   = input(f"  Email      [{target.email}]: ").strip()
            new_phone   = input(f"  Phone      [{target.phone}]: ").strip()
            new_address = input(f"  Address    [{target.address}]: ").strip()

            # Only update fields that were filled in
            if new_name:    target.full_name = new_name
            if new_email:   target.email     = new_email
            if new_phone:   target.phone     = new_phone
            if new_address: target.address   = new_address

            users[target.username] = target
            fh.save_users(users) # save the updated data
            ok("\n  Student updated successfully.")

        except Exception as e:
            err(f"  Error: {e}")

        input("\n  Press Enter to continue...")
