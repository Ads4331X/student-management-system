"""
OOP data classes for the Student Profile Management System.
Classes:
    User      — Base class for all users
    Student   — Inherits from User (role = student)
    Admin     — Inherits from User (role = admin)
"""

# list of subjects
SUBJECTS = ["mathematics", "science", "english", "programming", "data_science"]


class User:
    """Base class representing a system user (admin or student)."""

    def __init__(self, user_id, username, full_name, email, role, phone="", address=""):
        self.user_id = user_id
        self.username = username
        self.full_name = full_name
        self.email = email
        self.role = role
        self.phone = phone
        self.address = address

    def to_dict(self):
        """Return user data as a dictionary (for saving to CSV)."""
        return {
            "user_id": self.user_id,
            "username": self.username,
            "full_name": self.full_name,
            "email": self.email,
            "role": self.role,
            "phone": self.phone,
            "address": self.address,
        }

    def display(self):
        """Print a formatted summary of this user."""
        print(f"\n  ID       : {self.user_id}")
        print(f"  Name     : {self.full_name}")
        print(f"  Username : {self.username}")
        print(f"  Email    : {self.email}")
        print(f"  Phone    : {self.phone or 'N/A'}")
        print(f"  Address  : {self.address or 'N/A'}")
        print(f"  Role     : {self.role.capitalize()}")

    def __repr__(self):
        return f"User({self.user_id}, {self.username}, {self.role})"


class Student(User):
    """Student user — can view/update own data. Inherits from User."""

    def __init__(self, user_id, username, full_name, email, phone="", address=""):
        super().__init__(user_id, username, full_name, email, "student", phone, address)


class Admin(User):
    """Admin user — can manage all student records. Inherits from User."""

    def __init__(self, user_id, username, full_name, email, phone="", address=""):
        super().__init__(user_id, username, full_name, email, "admin", phone, address)