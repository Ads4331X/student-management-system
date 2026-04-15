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

    def view_grades(self):
        """Show the student's marks with a simple text bar chart."""
        clear_screen(); banner(); section("MY GRADES")

        try:
            # Fetch grades from file/database layer
            grades = fh.get_student_grades(self.user.user_id)

            # Convert subject marks to float list
            marks = [float(grades[s]) for s in SUBJECTS]

            # Compute average marks
            average = sum(marks) / len(marks)

            print(f"\n  Grades for {self.user.full_name}\n")
            print(f"  {'Subject':<18} {'Mark':>6}   Bar")
            print("  " + "─" * 50)

            # Print each subject with visual bar representation
            for s, m in zip(SUBJECTS, marks):
                bar = "█" * int(m / 5)
                print(f"  {s.capitalize():<18} {m:>6.1f}   {bar}")

            print("  " + "─" * 50)

            # Determine letter grade based on average
            grade = (
                "A" if average >= 80 else
                "B" if average >= 70 else
                "C" if average >= 60 else
                "D" if average >= 50 else
                "F"
            )

            print(f"  {'Average':<18} {average:>6.1f}   Grade: {grade}")

        except Exception as e:
            # Handle missing file or corrupted data
            err(f"  Error loading grades: {e}")

        input("\n\n  Press Enter to continue...")
