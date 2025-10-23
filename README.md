# Xpense - Expense Tracker Application

## Overview

Xpense is a desktop application for tracking personal expenses and income. It provides a user-friendly interface for adding, viewing, updating, and visualizing financial records. The app uses a MySQL database for data storage and offers features like CSV export, financial summaries, and interactive charts.

---

## Features

- **User Authentication:** Sign up and login system.
- **Expense Management:** Add, update, delete, and search expense records.
- **Financial Summary:** View total income, expenses, and available balance.
- **Data Visualization:** Pie chart and line graph for expense distribution and trends.
- **Export Data:** Export filtered expenses to CSV files.
- **Custom UI:** Modern interface using CustomTkinter.

---

## Requirements

- Python 3.8+
- MySQL Server (with a database named `budget_planning`)
- Required Python packages:
  - `customtkinter`
  - `matplotlib`
  - `mysql-connector-python`
  - `pandas`
  - `tkinter` (standard library)

Install dependencies via pip:

```bash
pip install customtkinter matplotlib mysql-connector-python pandas
```

---

## Database Setup

1. **Create Database:**
   - Name: `budget_planning`

2. **Create Table:**
   ```sql
   CREATE TABLE expense (
     id INT AUTO_INCREMENT PRIMARY KEY,
     userid VARCHAR(50),
     date DATETIME,
     title VARCHAR(100),
     expense_type VARCHAR(50),
     amount FLOAT,
     comment VARCHAR(255)
   );
   ```

---

## How to Run

1. **Configure MySQL Connection:**
   - Edit the connection settings at the top of `Expense-Tracker.py` if needed:
     ```python
     conn = mysql.connector.connect(
         database="budget_planning",
         user="root",
         host="localhost",
         password="",
         port=3307,
     )
     ```

2. **Start the Application:**
   ```bash
   python Expense-Tracker.py
   ```

---

## Usage Guide

1. **Login / Sign Up:**
   - On launch, create a new account or log in with existing credentials.

2. **Home Tab:**
   - Add new expense/income records.
   - View, search, update, or delete records.
   - Export data to CSV.

3. **Graph Tab:**
   - View financial summary (income, expenses, balance).
   - Visualize expense distribution and trends.

---

## Code Structure

- **first_page()**: Login screen.
- **signUp_page()**: Registration screen.
- **second_page(userid)**: Main dashboard after login.
- **fetch_expense_data(userid)**: Loads user’s expense data from the database.
- **add_record() / update_record() / remove_selected_record() / remove_all_records()**: CRUD operations for expenses.
- **calculate_balance()**: Computes and displays financial summary.
- **update_chart()**: Updates the expense distribution chart.
- **export_expenses()**: Exports filtered data to CSV.

---

## Notes

- Make sure MySQL server is running and accessible.
- The app uses CustomTkinter for a modern look; install it via pip if missing.
- For any issues, check the terminal for error messages.

---

## License

This project is for educational purposes.
