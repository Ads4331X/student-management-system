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

    def view_eca(self):
        """Show the student's ECA activities."""
        clear_screen(); banner(); section("MY ECA ACTIVITIES")

        try:
            # Fetch extracurricular activities list
            activities = fh.get_student_eca(self.user.user_id)

            # If no activities found
            if not activities:
                info("  No ECA activities recorded yet.")
            else:
                print()

                # Display all activities with numbering
                for i, act in enumerate(activities, 1):
                    print(f"  [{i}] {act}")

                print(f"\n  Total: {len(activities)} activities")

        except Exception as e:
            err(f"  Error: {e}")

        input("\n\n  Press Enter to continue...")

    def update_profile(self):
        """Allow the student to update their own email, phone, and address."""
        clear_screen(); banner(); section("UPDATE MY PROFILE")
        print("\n  (Press Enter to keep current value)\n")

        try:
            # Load all users from storage
            users = fh.load_users()

            # Get updated values from user input
            new_email   = input(f"  Email   [{self.user.email}]: ").strip()
            new_phone   = input(f"  Phone   [{self.user.phone}]: ").strip()
            new_address = input(f"  Address [{self.user.address}]: ").strip()

            # Update only if user entered new values
            if new_email:   self.user.email   = new_email
            if new_phone:   self.user.phone   = new_phone
            if new_address: self.user.address = new_address

            # Save updated user object back into dictionary
            users[self.user.username] = self.user
            fh.save_users(users)

            ok("\n  Profile updated successfully.")

        except Exception as e:
            # Handle file write or data issues
            err(f"  Error: {e}")

        input("\n  Press Enter to continue...")

    def view_grade_chart(self):
        """
        Display a matplotlib bar chart of the student's grades in a window.
        """
        clear_screen(); banner(); section("MY GRADE CHART")

        try:
            # Fetch grades for student
            grades = fh.get_student_grades(self.user.user_id)

            # Convert marks and labels
            marks  = [float(grades[s]) for s in SUBJECTS]
            labels = [s.capitalize() for s in SUBJECTS]

            # Calculate average score
            average = sum(marks) / len(marks)

            # Assign bar colors based on performance
            # Green: >=70, Orange: >=50, Red: <50
            colors = [
                "#4CAF50" if m >= 70 else
                "#FF9800" if m >= 50 else
                "#F44336"
                for m in marks
            ]

            # Create bar chart figure
            fig, ax = plt.subplots(figsize=(9, 5))
            bars = ax.bar(labels, marks, color=colors, edgecolor="white", linewidth=1.2)

            # Draw average line
            ax.axhline(
                y=average,
                color="#2196F3",
                linestyle="--",
                linewidth=1.8,
                label=f"Average: {average:.1f}"
            )

            # Draw pass mark line
            ax.axhline(
                y=50,
                color="red",
                linestyle=":",
                linewidth=1.2,
                alpha=0.6,
                label="Pass mark: 50"
            )

            # Annotate each bar with value
            for bar, m in zip(bars, marks):
                ax.text(
                    bar.get_x() + bar.get_width() / 2,
                    m + 1.5,
                    f"{m:.0f}",
                    ha="center",
                    va="bottom",
                    fontsize=10
                )

            # Chart formatting
            ax.set_ylim(0, 115)
            ax.set_ylabel("Marks", fontsize=11)
            ax.set_title(
                f"Grade Chart — {self.user.full_name}",
                fontsize=13,
                fontweight="bold"
            )
            ax.legend()

            plt.tight_layout()

            # Show the chart window
            plt.show()

        except Exception as e:
            err(f"  Error generating chart: {e}")

        input("\n\n  Press Enter to continue...")