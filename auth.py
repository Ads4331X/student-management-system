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

        """
        Remove a user and all their associated data.
        Returns (True, message) or (False, message).
        """
        try:
            users = fh.load_users()
            if username not in users:
                return False, "User not found."

            user = users[username]
            user_id = user.user_id

            # Remove from users and passwords
            del users[username]
            fh.save_users(users)

            passwords = fh.load_passwords()
            passwords.pop(username, None)
            fh.save_passwords(passwords)

            # Remove grades row
            import pandas as pd
            df = fh.load_grades()
            df = df[df["student_id"] != user_id]
            fh.save_grades(df)

            # Remove ECA entry
            eca = fh.load_eca()
            eca.pop(user_id, None)
            fh.save_eca(eca)

            return True, f"Student '{user.full_name}' deleted."

        except Exception as e:
            return False, f"Error deleting user: {e}"