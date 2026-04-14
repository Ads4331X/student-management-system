"""
display helpers
"""

import os

def clear_screen():
    """Clear the terminal screen."""
    os.system("cls" if os.name == "nt" else "clear")

def banner():
    """Print the system banner in cyan."""
    print("\033[36m")
    print("  ╔══════════════════════════════════════════╗")
    print("  ║                                          ║")
    print("  ║   STUDENT PROFILE MANAGEMENT SYSTEM      ║")
    print("  ║                                          ║")
    print("  ╚══════════════════════════════════════════╝")
    print("\033[0m", end="")

def section(title):
    """Print a section heading."""
    print(f"\n\033[1;33m  ── {title} ──\033[0m")

def ok(msg):
    """Print a success message in green."""
    print(f"\033[92m{msg}\033[0m")

def err(msg):
    """Print an error message in red."""
    print(f"\033[91m{msg}\033[0m")

def info(msg):
    """Print an info message in blue."""
    print(f"\033[94m{msg}\033[0m")
