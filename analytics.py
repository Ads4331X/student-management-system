"""
Performance Analytics Dashboard (Task 2 bonus).
Implement advanced analytics using pandas, numpy, matplotlib.

Features:
    - Grade trends per subject
    - ECA vs academic performance correlation
    - Performance alerts for at-risk students
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import file_handler as fh
from models import SUBJECTS
from utils import clear_screen, banner, section, ok, err, info

PASS_MARK = 50.0      # Below this = failing a subject
ALERT_AVG = 55.0      # Below this average = at-risk student


class AnalyticsDashboard:
    """Provides administrative analytics dashboard with charts and statistics."""

    # full dashboard 
    def show_dashboard(self):
        clear_screen(); banner(); section("ANALYTICS DASHBOARD") # UI setup

        try:
            # load datasets users, grades , ECA
            df = fh.load_grades()
            users = fh.load_users()
            eca = fh.load_eca()

            if df.empty: # check if grade is empty
                info("  No grade data available.")
                input("\n  Press Enter to continue...")
                return
        except Exception as e:
            err(f"  Dashboard error: {e}")

        input("\n\n  Press Enter to continue...")
