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

    #  view sll dtudents 
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

    # delete student 
    def delete_student(self):
        """Delete a student and all their data after confirmation."""
        clear_screen(); banner(); section("DELETE STUDENT")

        try:
            # gets student_id from the admin
            uid = input("  Enter Student ID to delete: ").strip().upper()
            user = fh.get_user_by_id(uid) # gets the user from its id

            if not user or user.role != "student": # not found
                err(f"  Student '{uid}' not found.")
                input("\n  Press Enter to continue...")
                return

            print(f"\n  About to delete: {user.full_name} ({uid})")
            confirm = input("  Type YES to confirm: ").strip()

            if confirm == "YES":
                success, msg = self.auth.delete_user(user.username) # delete the user
                ok(f"  {msg}") if success else err(f"  {msg}")
            else:
                info("  Deletion cancelled.")

        except Exception as e:
            err(f"  Error: {e}")

        input("\n  Press Enter to continue...")

    # update grades 
    def update_grades(self):
        """Enter or update marks for a student across all five subjects."""
        clear_screen(); banner(); section("UPDATE GRADES")

        try:
            # gets student_id from the admin
            uid = input("  Enter Student ID: ").strip().upper()
            user = fh.get_user_by_id(uid) # gets user from its id

            if not user or user.role != "student": # not found
                err(f"  Student '{uid}' not found.")
                input("\n  Press Enter to continue...")
                return

            current = fh.get_student_grades(uid) # get existing grades for the student
            # Display current grades in a formatted table
            print(f"\n  Current grades for {user.full_name}:")
            print(f"\n  {'Subject':<18} {'Current':>8}")
            print("  " + "─" * 28)
            for s in SUBJECTS: 
                print(f"  {s.capitalize():<18} {current[s]:>8.1f}")

            print("\n  Enter new marks (0-100). Press Enter to keep current.\n")
             
            new_marks = {}  # Dictionary to store updated grades

             # Loop through each subject and get new marks
            for s in SUBJECTS:
                while True:
                    val = input(f"  {s.capitalize()} [{current[s]:.1f}]: ").strip()
                    if val == "": # Keep existing value if input is empty
                        new_marks[s] = current[s]
                        break
                    try:
                        m = float(val)
                        if 0 <= m <= 100: # Validate mark range
                            new_marks[s] = m
                            break
                        else:
                            err("  Must be between 0 and 100.")
                    except ValueError:
                        err("  Enter a valid number.")

            fh.upsert_student_grades(uid, new_marks) # Save updated grades 
            ok("\n  Grades updated successfully.")

        except Exception as e: # Catch unexpected errors and display message
            err(f"  Error: {e}")

        input("\n  Press Enter to continue...")

    # update ECA 
    def update_eca(self):
        """Add or remove ECA activities for a student."""
        clear_screen(); banner(); section("UPDATE ECA") # clear screen , display banner and 

        try:
            # gets student_id from the admin
            uid = input("  Enter Student ID: ").strip().upper()
            user = fh.get_user_by_id(uid) # Fetch user object using student ID

            if not user or user.role != "student": # not found
                err(f"  Student '{uid}' not found.")
                input("\n  Press Enter to continue...")
                return

            activities = fh.get_student_eca(uid) # Retrieve existing eca for the student
            # Display current ECA activities
            print(f"\n  ECA for {user.full_name}:")
            if activities:
                for i, a in enumerate(activities, 1):
                    print(f"  [{i}] {a}")
            else:
                info("  No activities yet.")

            print("\n  [1] Add activity  [2] Remove activity  [3] Clear all  [0] Cancel") # menu
            choice = input("\n  Choice: ").strip() 

            # add a new activity
            if choice == "1":
                name = input("  Activity name: ").strip()
                if name: # validate activity name
                    activities.append(name)
                    fh.upsert_student_eca(uid, activities)
                    ok(f"  Added: {name}")
                else:
                    err("  Activity name cannot be empty.")

            # remove a activity
            elif choice == "2":
                if not activities:
                    info("  Nothing to remove.")
                else:
                    try:
                        idx = int(input("  Enter number to remove: ").strip()) - 1 # Convert user input to list index
                        if 0 <= idx < len(activities): # Validate index range
                            removed = activities.pop(idx)
                            fh.upsert_student_eca(uid, activities)
                            ok(f"  Removed: {removed}")
                        else:
                            err("  Invalid number.")
                    except ValueError:
                        err("  Enter a valid number.")
            # clear all activities
            elif choice == "3":
                fh.upsert_student_eca(uid, [])
                ok("  All activities cleared.")

        except Exception as e:
            # Handle unexpected runtime errors
            err(f"  Error: {e}")

        input("\n  Press Enter to continue...")
        
    # grade insights 
    def view_insights(self):
        """
        Show grade statistics using numpy and pandas:
        - Subject averages, highest, lowest
        - Student ranking by average
        - ECA participation count
        """
        clear_screen(); banner(); section("GRADE INSIGHTS")

        try:
            # load grades users and ECA
            df_grades = fh.load_grades()
            users = fh.load_users()
            eca = fh.load_eca()

            if df_grades.empty: # check if grade data exists
                info("  No grade data available.")
                input("\n  Press Enter to continue...")
                return

            # Subject stats using numpy 
            print("\n  SUBJECT STATISTICS (numpy)\n")
            # print table header
            print(f"  {'Subject':<18} {'Average':>8}  {'Highest':>8}  {'Lowest':>7}  {'Std Dev':>8}")
            print("  " + "─" * 60)
            # compute statistics for each subject
            for s in SUBJECTS:
                marks = df_grades[s].astype(float).values
                print(f"  {s.capitalize():<18} "
                      f"{np.mean(marks):>8.1f}  "
                      f"{np.max(marks):>8.1f}  "
                      f"{np.min(marks):>7.1f}  "
                      f"{np.std(marks):>8.1f}")

            # Student ranking using pandas 
            df = df_grades.copy()
            # compute student average across all subjects
            df["average"] = df[SUBJECTS].astype(float).mean(axis=1)
            # sort students by performance 
            df = df.sort_values("average", ascending=False).reset_index(drop=True)

            print("\n\n  STUDENT RANKING (pandas)\n")
            print(f"  {'Rank':<6} {'ID':<8} {'Name':<22} {'Average':>8}  {'Grade'}")
            print("  " + "─" * 56)

            # display ranking table
            for rank, row in df.iterrows():
                sid = row["student_id"]
                user = users.get(next((u for u in users if users[u].user_id == sid), ""), None) # find user object for name mapping
                name = user.full_name if user else sid
                avg = row["average"]
                # Assign grade based on average
                grade = (
                "A" if avg >= 80 else
                "B" if avg >= 70 else
                "C" if avg >= 60 else
                "D" if avg >= 50 else
                "F"
                )
                print(f"  {rank+1:<6} {sid:<8} {name:<22} {avg:>8.1f}  {grade}")

            # ECA participation 
            print("\n\n  ECA PARTICIPATION\n")
            # sort students by number of activities 
            for sid, acts in sorted(eca.items(), key=lambda x: len(x[1]), reverse=True):
                user = fh.get_user_by_id(sid)
                name = user.full_name if user else sid
                # Visual indicator using dots
                print(f"  {name:<22}: {len(acts)} activities  {'●' * len(acts)}")

        except Exception as e: # Catch unexpected errors
            err(f"  Error: {e}")

        input("\n\n  Press Enter to continue...") # Pause before returning
