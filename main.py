"""
Entry point for the Student Profile Management System
"""
from utils import clear_screen, banner, section, ok, err


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
