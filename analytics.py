"""
Performance Analytics Dashboard
Implement advanced analytics using pandas, numpy, matplotlib

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

            # build matplotlib dashboard 
            fig, axes = plt.subplots(2, 2, figsize=(13, 9))  # Create 2x2 subplot layout
            fig.suptitle("Performance Analytics Dashboard", fontsize=15, fontweight="bold")
            plt.subplots_adjust(hspace=0.4, wspace=0.35) # Adjust spacing between plots

            # pannel-1
            # Subject averages bar chart
            ax1 = axes[0, 0]
            subj_means = [df[s].astype(float).mean() for s in SUBJECTS] # calculate mean score per subject
            # Colors based on performance level
            colors1 = [
                "#4CAF50" if m >= 70 else
                "#FF9800" if m >= 50 else
                "#F44336"
                for m in subj_means
            ]
            # Plot bar chart for subject averages
            ax1.bar(
                [s[:6].capitalize() for s in SUBJECTS],
                subj_means,
                color=colors1,
                edgecolor="white"
            )
            # Pass mark reference line
            ax1.axhline(
                y=PASS_MARK,
                color="red",
                linestyle="--",
                alpha=0.5,
                label="Pass mark"
            )

            ax1.set_title("Subject Averages", fontweight="bold")
            ax1.set_ylabel("Average Mark")
            ax1.set_ylim(0, 105)
            ax1.legend(fontsize=8)
            for i, v in enumerate(subj_means): # add values labels above the bar
                ax1.text(i, v + 1, f"{v:.1f}", ha="center", fontsize=9)

            # pannel-2
            # Per-student average (horizontal bar)
            ax2 = axes[0, 1]
            names = [] # list to store names
            for sid in df["student_id"]: # extract student name
                u = fh.get_user_by_id(sid) # get user by its id
                names.append(u.full_name.split()[0] if u else sid) # if name not found use student_id
            avgs = df["average"].values
            # Color-code students based on performance
            colors2 = [
                "#4CAF50" if a >= 70 else
                "#FF9800" if a >= 50 else
                "#F44336"
                for a in avgs
            ]
            # Horizontal bar chart for student averages
            ax2.barh(names, avgs, color=colors2, edgecolor="white")
            # Pass mark reference line
            ax2.axvline(
                x=PASS_MARK,
                color="red",
                linestyle="--",
                alpha=0.5,
                label="Pass mark"
            )
            ax2.set_title("Student Averages", fontweight="bold")
            ax2.set_xlabel("Average Mark")
            ax2.set_xlim(0, 105)
            ax2.legend(fontsize=8)

        except Exception as e:
            err(f"  Dashboard error: {e}")

        input("\n\n  Press Enter to continue...")

  
  