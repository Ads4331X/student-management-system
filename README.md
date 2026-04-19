# Student Profile Management System

## What Does This Program Do?

This is a **command-line student management system** built in Python.

- **Admins** can add, update, and delete student records, manage grades and ECA activities, and view analytics charts
- **Students** can view their own profile, grades, and ECA activities, and update their contact information
- All data is stored in **4 CSV files** (no database needed)
- An **analytics dashboard** shows grade trends, ECA correlation, and performance alerts using pandas, numpy, and matplotlib

---

## How to Run

### Step 1 — Install Python libraries

```bash
pip install pandas numpy matplotlib
```

### Step 2 — Run the program

```bash
python main.py
```

### Step 3 — Login with one of these accounts

| Role    | Username | Password   |
| ------- | -------- | ---------- |
| Admin   | `admin`  | `admin123` |
| Student | `john`   | `john123`  |
| Student | `jane`   | `jane123`  |
| Student | `ram`    | `ram123`   |

---

## Project File Structure

```
student_management_system/
│
├── main.py
├── auth.py
├── models.py
├── admin.py
├── student.py
├── analytics.py
├── file_handler.py
├── utils.py
├── requirements.txt
├── .gitignore
├── README.md
│
├── data/
│   ├── users.csv
│   ├── passwords.csv
│   ├── grades.csv
│   └── eca.csv
│
└── docs/
    ├── Report.docx
    ├── Presentation.pptx
    └── flowcharts.mmd
```

---

## What Each File Does

### `main.py` — Entry point

Starts the program. Shows the main menu (Login / Exit). After successful login, routes the user to either the **Admin menu** or **Student portal** depending on their role. Allows maximum **3 login attempts** before returning to main menu.

### `auth.py` — Authentication

- `login()` — checks username against `passwords.csv` and `users.csv`, returns a User object or None
- `register_student()` — validates uniqueness of ID and username, then saves to all 4 CSV files
- `delete_user()` — removes a student from all 4 CSV files at once

### `models.py` — OOP Classes

Three classes using **inheritance**:

- `User` (base class) — holds common fields: user_id, username, full_name, email, role, phone, address
- `Student(User)` — inherits everything, role is fixed to `"student"`
- `Admin(User)` — inherits everything, role is fixed to `"admin"`

### `admin.py` — Admin panel

Nine operations available from the admin menu:

1. Add new student
2. View all students
3. Update student profile
4. Delete student
5. Update student grades
6. Update student ECA activities
7. View grade insights (numpy stats + pandas ranking)
8. Analytics dashboard (matplotlib charts)
9. Performance alerts (at-risk students)

### `student.py` — Student portal

Five operations available from the student menu:

1. View my profile
2. View my grades (with text bar chart)
3. View my ECA activities
4. Update my profile (email, phone, address only)
5. View my grade chart (matplotlib bar chart)

### `analytics.py` — Analytics dashboard (Task 2)

- **show_dashboard()** — displays a 4-panel matplotlib chart: subject averages, student averages, ECA vs grade scatter plot with trend line, and grade distribution pie chart
- **performance_alerts()** — filters students below 55% average using pandas, finds failing subjects using numpy, and suggests personalised interventions

### `file_handler.py` — All file I/O

The **only** file that reads and writes CSV data. All other modules call functions here instead of touching files directly. Uses pandas for all operations.

### `utils.py` — Display helpers

Functions for clearing the screen, printing the banner (cyan), section headings (yellow), success messages (green), error messages (red), and info messages (blue).

---

## Data File Formats

### `users.csv`

```
user_id,username,full_name,email,role,phone,address
A001,admin,System Administrator,admin@email.edu,admin,9800000000,test Office
S001,john,John Doe,john@email.edu,student,9800000001,Kathmandu
```

### `passwords.csv`

```
username,password
admin,admin123
john,john123
```

### `grades.csv`

```
student_id,mathematics,science,english,programming,data_science
S001,78.0,85.0,72.0,90.0,88.0
```

### `eca.csv`

Activities are separated by semicolons inside one cell.

```
student_id,activities
S001,Football Club;Debate Society;Coding Club
```

---

## Grade Scale

| Average Score | Letter Grade |
| ------------- | ------------ |
| 80 and above  | A            |
| 70 – 79       | B            |
| 60 – 69       | C            |
| 50 – 59       | D            |
| Below 50      | F            |

---

## OOP Concepts Used

| Concept                | Where                                                                                        |
| ---------------------- | -------------------------------------------------------------------------------------------- |
| **Class**              | `User`, `Student`, `Admin`, `AuthSystem`, `AdminPanel`, `StudentPanel`, `AnalyticsDashboard` |
| **Inheritance**        | `Student` and `Admin` both inherit from `User`                                               |
| **Encapsulation**      | `file_handler.py` is the only module that accesses CSV files                                 |
| **Methods**            | Every class has clearly defined methods for each operation                                   |
| **Exception handling** | `try/except` in every method that touches files or user input                                |

---

## Libraries Used

| Library      | Purpose                                                                                                        |
| ------------ | -------------------------------------------------------------------------------------------------------------- |
| `pandas`     | Reading/writing CSV files as DataFrames, computing averages, filtering at-risk students                        |
| `numpy`      | Statistical functions (mean, std, max, min), Pearson correlation, trend line fitting, finding failing subjects |
| `matplotlib` | Bar charts, horizontal bar charts, scatter plots, pie charts                                                   |

---

## Team Contributions

| Member            | Files / Tasks                                                                                                  |
| ----------------- | -------------------------------------------------------------------------------------------------------------- |
| [Adarsha Karki]   | [main.py, utils.py, student.py, analytics.py: Student portal, display helpers, analytics dashboard and charts] |
| [Bishesh Thapa]   | [models.py, file_handler.pyOOP class design and all CSV file handling]                                         |
| [Jonisha Ghimire] | [auth.py, admin.pyLogin system and full admin panel]                                                           |

---

## Reflection

**[Adarsha Karki]:**
Building the analytics dashboard with numpy and matplotlib was the most interesting part. The hardest bit was getting the scatter plot trend line working correctly.
**[Bishesh Thapa]:**
Designing the OOP inheritance structure (Student and Admin extending User) taught me a lot. The trickiest part was making upsert work without creating duplicate rows.
**[Jonisha Ghimire]:**
Connecting the login system to the admin panel was challenging. Deleting a student across all four CSV files at once was the hardest function to get right.

---

## Known Limitations

- Passwords are stored in plain text (acceptable for learning purposes as per the brief)
- No concurrent access support — designed for single user at a time
- Charts open in a separate matplotlib window and pause the terminal until closed
- The `.gitignore` excludes the `data/` folder — copy clean CSV files manually after cloning
