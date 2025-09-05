import streamlit as st
import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# Database connection
def get_connection():
    return mysql.connector.connect(
        database="budget_planning",
        user="root",
        host="localhost",
        password="",
        port=3307,
    )

# User authentication
def authenticate_user(userid, password):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT userid FROM userinfo WHERE userid = %s AND password = %s", (userid, password))
    user = cur.fetchone()
    cur.close()
    conn.close()
    return user is not None

def create_user(userid, name, password):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT userid FROM userinfo WHERE userid = %s", (userid,))
    if cur.fetchone():
        cur.close()
        conn.close()
        return False, "User ID already exists."
    cur.execute("INSERT INTO userinfo (userid, password, user_name) VALUES (%s, %s, %s)", (userid, password, name))
    conn.commit()
    cur.close()
    conn.close()
    return True, "Account created successfully!"

# Expense operations
def add_expense(userid, title, category, amount, comment):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO expense (userid, date, title, expense_type, amount, comment) VALUES (%s, %s, %s, %s, %s, %s)",
        (userid, datetime.now().strftime("%Y-%m-%d"), title, category, amount, comment),
    )
    conn.commit()
    cur.close()
    conn.close()

def get_expenses(userid, search_term=None):
    conn = get_connection()
    cur = conn.cursor()
    if search_term:
        cur.execute(
            "SELECT id, title, expense_type, amount, comment FROM expense WHERE userid = %s AND (expense_type LIKE %s OR comment LIKE %s OR title LIKE %s) ORDER BY id DESC",
            (userid, f"%{search_term}%", f"%{search_term}%", f"%{search_term}%")
        )
    else:
        cur.execute(
            "SELECT id, title, expense_type, amount, comment FROM expense WHERE userid = %s ORDER BY id DESC LIMIT 20",
            (userid,)
        )
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows

def update_expense(record_id, title, category, amount, comment):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "UPDATE expense SET title = %s, expense_type = %s, amount = %s, comment = %s WHERE id = %s",
        (title, category, amount, comment, record_id)
    )
    conn.commit()
    cur.close()
    conn.close()

def remove_expense(record_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM expense WHERE id = %s", (record_id,))
    conn.commit()
    cur.close()
    conn.close()

def remove_all_expenses(userid):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM expense WHERE userid = %s", (userid,))
    conn.commit()
    cur.close()
    conn.close()

def get_summary(userid):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT SUM(amount) FROM expense WHERE userid = %s AND expense_type IN ('Income', 'Allowance')", (userid,))
    total_income = cur.fetchone()[0] or 0.0
    cur.execute("SELECT SUM(amount) FROM expense WHERE userid = %s AND expense_type NOT IN ('Income', 'Allowance')", (userid,))
    total_expenses = cur.fetchone()[0] or 0.0
    cur.close()
    conn.close()
    balance = total_income - total_expenses
    return total_income, total_expenses, balance

def get_expense_distribution(userid):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT expense_type, SUM(amount) FROM expense WHERE userid = %s AND expense_type NOT IN ('Income', 'Allowance') GROUP BY expense_type",
        (userid,))
    data = cur.fetchall()
    cur.close()
    conn.close()
    return data

# Streamlit UI
st.set_page_config(page_title="Xpense Tracker", layout="wide")
st.title("Xpense Tracker")

if "userid" not in st.session_state:
    st.session_state.userid = None

def login_page():
    st.header("Login")
    userid = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if authenticate_user(userid, password):
            st.session_state.userid = userid
            st.success("Login successful!")
            st.rerun()
        else:
            st.error("Invalid username or password.")
    if st.button("Create New Account"):
        st.session_state.show_signup = True

def signup_page():
    st.header("Sign Up")
    userid = st.text_input("Username", key="signup_userid")
    name = st.text_input("Full Name", key="signup_name")
    password = st.text_input("Password", type="password", key="signup_password")
    if st.button("Create Account"):
        success, msg = create_user(userid, name, password)
        if success:
            st.success(msg)
            st.session_state.userid = userid
            st.session_state.show_signup = False
            st.rerun()
        else:
            st.error(msg)
    if st.button("Back to Login"):
        st.session_state.show_signup = False

if st.session_state.userid is None:
    if "show_signup" in st.session_state and st.session_state.show_signup:
        signup_page()
    else:
        login_page()
    st.stop()

st.sidebar.header(f"Welcome, {st.session_state.userid}!")
if st.sidebar.button("Logout"):
    st.session_state.userid = None
    st.experimental_rerun()

tab1, tab2 = st.tabs(["🏠 Home", "📊 Graph"])

with tab1:
    st.subheader("Add Expense/Income")
    with st.form("add_record_form"):
        title = st.text_input("Title*")
        amount = st.text_input("Amount*")
        category = st.selectbox("Category*", [
            "Income", "Allowance", "Supermarket", "Transport", "Shopping", 
            "Foods", "Drinks", "Restaurants", "Cafes", "Fast Food", "Online services",
            "Housing and utilities", "Transfers to other people", "Other"
        ])
        comment = st.text_input("Comment")
        submitted = st.form_submit_button("Add Record")
        if submitted:
            if not title or not amount or not category:
                st.error("Please fill in all required fields.")
            else:
                try:
                    amt = float(amount)
                    if amt <= 0:
                        st.error("Amount must be greater than 0.")
                    else:
                        add_expense(st.session_state.userid, title, category, amt, comment)
                        st.success(f"Record added: {category} ₱{amt:,.2f}")
                except ValueError:
                    st.error("Amount must be a number.")

    st.subheader("Expense Records")
    search_term = st.text_input("Search by title, category, or comment")
    if st.button("Search"):
        records = get_expenses(st.session_state.userid, search_term)
    else:
        records = get_expenses(st.session_state.userid)
    df = pd.DataFrame(records, columns=["ID", "Title", "Category", "Amount", "Comment"])
    st.dataframe(df, use_container_width=True)

    st.subheader("Update or Remove Record")
    record_id = st.text_input("Record ID to update/remove")
    update_col1, update_col2 = st.columns(2)
    with update_col1:
        new_title = st.text_input("New Title", key="update_title")
        new_amount = st.text_input("New Amount", key="update_amount")
        new_category = st.selectbox("New Category", [
            "Income", "Allowance", "Supermarket", "Transport", "Shopping", 
            "Foods", "Drinks", "Restaurants", "Cafes", "Fast Food", "Online services",
            "Housing and utilities", "Transfers to other people", "Other"
        ], key="update_category")
        new_comment = st.text_input("New Comment", key="update_comment")
        if st.button("Update Record"):
            if not record_id or not new_title or not new_amount or not new_category:
                st.error("Please fill in all required fields for update.")
            else:
                try:
                    amt = float(new_amount)
                    update_expense(record_id, new_title, new_category, amt, new_comment)
                    st.success("Record updated successfully!")
                except Exception as e:
                    st.error(f"Error updating record: {e}")
    with update_col2:
        if st.button("Remove Selected Record"):
            if not record_id:
                st.error("Please enter a Record ID to remove.")
            else:
                try:
                    remove_expense(record_id)
                    st.success("Record removed successfully!")
                except Exception as e:
                    st.error(f"Error removing record: {e}")
        if st.button("Remove All Records"):
            if st.confirm("Are you sure you want to remove ALL records? This cannot be undone!"):
                remove_all_expenses(st.session_state.userid)
                st.success("All records removed successfully!")

with tab2:
    st.subheader("Financial Summary")
    total_income, total_expenses, balance = get_summary(st.session_state.userid)
    st.metric("Total Income + Allowance", f"₱{total_income:,.2f}")
    st.metric("Total Expenses", f"₱{total_expenses:,.2f}")
    st.metric("Available Balance", f"₱{balance:,.2f}")

    st.subheader("Expense Distribution")
    data = get_expense_distribution(st.session_state.userid)
    if data:
        labels = [row[0] for row in data]
        sizes = [row[1] for row in data]
        fig, ax = plt.subplots()
        ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
        ax.axis('equal')
        st.pyplot(fig)
    else:
        st.info("No expense data available. Add some expenses to see the chart.")