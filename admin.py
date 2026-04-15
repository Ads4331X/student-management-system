"""
Admin panel: manage users, grades, ECA, and view insights.
Implement all admin operations.

Uses pandas for grade insights and numpy for basic statistics.
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

    #  View All Students 
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
