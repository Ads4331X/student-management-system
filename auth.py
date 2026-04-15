"""
Login and user registration logic.
"""

import file_handler as fh
from models import Student


class AuthSystem:
    """Handles login validation and new user registration."""

    def login(self, username, password):
        """
        Validate username and password.
        Returns the User object on success, or None on failure.
        Uses exception handling in case CSV files are missing/corrupt.
        """
        try:
            passwords = fh.load_passwords() # loads passwords
            users = fh.load_users() # loads user

            # Check credentials
            if username not in passwords or passwords[username] != password:
                return None
            if username not in users:
                return None

            return users[username]

        except Exception as e:
            print(f"  [Auth Error] {e}")
            return None

    def register_student(self, user_id, username, full_name, email, phone, address, password):
        """
        Register a new student.
        Returns (True, success_message) or (False, error_message).
        """
        try:
            users = fh.load_users() # loads users {username: user obj}
            passwords = fh.load_passwords() # loads passwords {username: password}

            # Validate uniqueness
            if username in users:
                return False, f"Username '{username}' already exists."
            if any(u.user_id == user_id for u in users.values()):
                return False, f"ID '{user_id}' already exists."

            # Create and save student
            student = Student(user_id, username, full_name, email, phone, address)
            users[username] = student
            fh.save_users(users)

            # Save password
            passwords[username] = password
            fh.save_passwords(passwords)

            # Initialize empty grades and ECA
            fh.upsert_student_grades(user_id, {s: 0.0 for s in ["mathematics", "science", "english", "programming", "data_science"]})
            fh.upsert_student_eca(user_id, [])

            return True, f"Student '{full_name}' added successfully."

        except Exception as e:
            return False, f"Error registering user: {e}"
