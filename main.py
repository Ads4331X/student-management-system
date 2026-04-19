"""
Entry point for the Student Profile Management System.

Default logins:
    username / password
       admin / admin123
       john  / john123
       jane  / jane123
       ram   / ram123
"""

import sys
from auth import AuthSystem
from admin import AdminPanel
from student import StudentPanel
from analytics import AnalyticsDashboard
from utils import clear_screen, banner, section, ok, err, info


def main():
    """Main loop  show landing screen and handle login."""
    auth = AuthSystem()

    while True:
        clear_screen() # clears the screen
        banner()  # displays the banner
        # menu
        print("\n  [1] Login")
        print("  [2] Exit")
        choice = input("\n  Choice: ").strip() # input choise of user

        if choice == "1":
            user = login_screen(auth) 
            if user:
                if user.role == "admin":
                    admin_menu(user) # display admin menu
                else:
                    student_menu(user) # display student menu
        elif choice == "2":
            info("\n  Goodbye!\n") 
            sys.exit(0)


def login_screen(auth):
    """Prompt for credentials up to 3 times. Returns User or None."""
    clear_screen(); banner(); section("LOGIN") # clears screen , displays banner and shows selection of login

    for attempt in range(1, 4): # max attempts = 3
        print(f"\n  Attempt {attempt}/3")
        # takes user input for username and password
        username = input("  Username: ").strip()
        password = input("  Password: ").strip()

        user = auth.login(username, password) #  Validate username and password.
        if user: # user is found
            ok(f"\n  Welcome, {user.full_name}! [{user.role.upper()}]") # success
            input("  Press Enter to continue...")
            return user
        else:
            err("  Incorrect username or password.") # error

    err("\n  Too many failed attempts.") # if attempt > 3 
    input("  Press Enter to return to main menu...")
    return None


def admin_menu(user):
    """Admin menu loop."""
    panel     = AdminPanel(user)
    dashboard = AnalyticsDashboard()

    options = {
        "1": ("Add New Student",          panel.add_student),
        "2": ("View All Students",         panel.view_all_students),
        "3": ("Update Student Profile",    panel.update_student),
        "4": ("Delete Student",            panel.delete_student),
        "5": ("Update Student Grades",     panel.update_grades),
        "6": ("Update Student ECA",        panel.update_eca),
        "7": ("View Grade Insights",       panel.view_insights),
        "8": ("Analytics Dashboard",       dashboard.show_dashboard),
        "9": ("Performance Alerts",        dashboard.performance_alerts),
        "0": ("Logout",                    None),
    }

    while True:
        clear_screen(); banner() # clear screen and displays banner
        print(f"\n  ADMIN PANEL — {user.full_name}\n")
        for key, (label, _) in options.items():
            print(f"  [{key}] {label}")

        choice = input("\n  Choice: ").strip()
        if choice == "0":
            return
        elif choice in options:
            options[choice][1]()
        else:
            err("  Invalid choice.")
            input("  Press Enter to continue...")


def student_menu(user):
    """Student menu loop."""
    panel = StudentPanel(user)

    options = {
        "1": ("View My Profile",      panel.view_profile),
        "2": ("View My Grades",       panel.view_grades),
        "3": ("View My ECA",          panel.view_eca),
        "4": ("Update My Profile",    panel.update_profile),
        "5": ("View My Grade Chart",  panel.view_grade_chart),
        "0": ("Logout",               None),
    }

    while True:
        clear_screen(); banner() # clear screen and display banner
        print(f"\n  STUDENT PORTAL — {user.full_name}\n")
        for key, (label, _) in options.items():
            print(f"  [{key}] {label}")

        choice = input("\n  Choice: ").strip()
        if choice == "0":
            return
        elif choice in options:
            options[choice][1]()
        else:
            err("  Invalid choice.")
            input("  Press Enter to continue...")


if __name__ == "__main__":
    main()

