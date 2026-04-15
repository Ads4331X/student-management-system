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
        """
        Display a 4-panel matplotlib dashboard:
        1. Subject averages (bar)
        2. Student averages (horizontal bar)
        3. ECA vs grade average (scatter)
        4. Grade letter distribution (pie)
        """
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

            # converts subjects col into float
            df_num = df[SUBJECTS].astype(float)
            df["average"] = df_num.mean(axis=1) # calculate average

            print("\n  SUBJECT AVERAGES\n")

            # print table header
            print(f"  {'Subject':<18} {'Mean':>7}  {'Max':>6}  {'Min':>6}  {'Std':>6}")
            print("  " + "─" * 50)
            for s in SUBJECTS:
                col = df[s].astype(float)
                print(f"  {s.capitalize():<18} {col.mean():>7.1f}  {col.max():>6.1f}  {col.min():>6.1f}  {col.std():>6.1f}")

            # ECA correlation 
            # counts the number of ECA per student 
            eca_counts = {sid: len(acts) for sid, acts in eca.items()}
            # map ECA counts to dataframe (missing values become 0)
            df["eca_count"] = df["student_id"].map(eca_counts).fillna(0)

            # calculates correlation
            correlation = np.corrcoef(df["eca_count"].values, df["average"].values)[0, 1]
            print(f"\n  ECA ↔ Grade correlation coefficient: {correlation:.3f}")

            # categorize the correlation
            if correlation > 0.3:
                info("  Positive trend: more ECA activities → higher grades.")
            elif correlation < -0.3:
                info("  Negative trend: more ECA activities → lower grades.")
            else:
                info("  No strong correlation between ECA and grades.")
        except Exception as e:
            err(f"  Dashboard error: {e}")

        input("\n\n  Press Enter to continue...")
   