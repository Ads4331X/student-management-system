"""
Student portal: view/update profile, grades, ECA, and charts.
Implement the student-facing interface.

Uses matplotlib for grade bar charts.
"""

import matplotlib.pyplot as plt

import file_handler as fh
from models import SUBJECTS
from utils import clear_screen, banner, section, ok, err, info


class StudentPanel:
    """Student operations: view profile, grades, ECA, and personal chart."""

    def __init__(self, user):
        # Store logged-in student user object
        self.user = user

    def view_profile(self):
        """Display the student's personal information."""
        clear_screen(); banner(); section("MY PROFILE")

        # Display user details using model method
        self.user.display()

        input("\n\n  Press Enter to continue...")
