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

    # add new student
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
