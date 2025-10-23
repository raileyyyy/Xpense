import tkinter as tk
import customtkinter as ctk
# from PIL import ImageTk, Image
import mysql.connector
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk
from datetime import datetime

conn = mysql.connector.connect(
    database="budget_planning",
    user="root",
    host="localhost",
    password="",
    port=3307,
)

def fetch_expense_data(userid):
    cur = conn.cursor()
    cur.execute("""
        SELECT id, userid, date, title, expense_type, amount, comment
        FROM expense
        WHERE userid = %s
        ORDER BY date ASC
    """, (userid,))
    rows = cur.fetchall()
    columns = [desc[0] for desc in cur.description]
    df = pd.DataFrame(rows, columns=columns)    
    # Ensure 'date' is datetime
    df['date'] = pd.to_datetime(df['date'])
    return df

app = ctk.CTk()
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")
app.geometry("1440x820")
app.title("Xpense")

# Custom color palette
PRIMARY_COLOR = "#39ace7"
SECONDARY_COLOR = "#0784b5" 
DARK_COLOR = "#414c50"
DARKER_COLOR = "#2d383c"
DARKEST_COLOR = "#192428"

def clear_window():
    """Clear all widgets from the window"""
    for widget in app.winfo_children():
        widget.destroy()

def logout_confirmation():
    """Show logout confirmation dialog"""
    if tk.messagebox.askyesno("Logout Confirmation", "Are you sure you want to logout?"):
        first_page()

def second_page(userid):
    clear_window()
    
    # Variables to store references
    table_data = []
    selected_record_id = None
    
    # Create main container
    main_frame = ctk.CTkFrame(app, fg_color=DARKEST_COLOR)
    main_frame.pack(fill="both", expand=True, padx=10, pady=10)
    
    # Header frame with logout button
    header_frame = ctk.CTkFrame(main_frame, height=50, fg_color=DARK_COLOR)
    header_frame.pack(fill="x", padx=0, pady=(0, 10))
    header_frame.pack_propagate(False)
    
    # Welcome label
    welcome_label = ctk.CTkLabel(header_frame, text=f"Welcome, {userid}!", 
                                font=("Arial", 16, "bold"), text_color="white")
    welcome_label.pack(side="left", padx=20, pady=15)
    
    # Logout button with confirmation
    logout_btn = ctk.CTkButton(header_frame, text="Logout", 
                              fg_color="#f44336", hover_color="#da190b",
                              width=80, height=30, command=logout_confirmation)
    logout_btn.pack(side="right", padx=20, pady=10)
    
    # Create tabview
    tabview = ctk.CTkTabview(main_frame, width=980, height=630, 
                            fg_color=DARKER_COLOR, segmented_button_fg_color=DARK_COLOR,
                            segmented_button_selected_color=PRIMARY_COLOR)
    tabview.pack(pady=0, padx=0, fill="both", expand=True)
    
    # Add tabs
    home_tab = tabview.add("🏠 Home")
    graph_tab = tabview.add("📊 Graph")
    
    # ==================== HOME TAB ====================
    def setup_home_tab():
        # Configure the tab background
        home_tab.configure(fg_color=DARKER_COLOR)
        
        # Top section with input fields
        input_frame = ctk.CTkFrame(home_tab, fg_color=DARK_COLOR, height=150)
        input_frame.pack(fill="x", padx=10, pady=(10, 5))
        input_frame.pack_propagate(False)
        
        # Left side - Budget Tracker logo and icon
        left_section = ctk.CTkFrame(input_frame, fg_color="transparent", width=120)
        left_section.pack(side="left", fill="y", padx=10, pady=10)
        left_section.pack_propagate(False)
        
        # Calculator icon
        icon_label = ctk.CTkLabel(left_section, text="🧮", font=("Arial", 40))
        icon_label.pack(pady=(10, 5))
        
        title_label = ctk.CTkLabel(left_section, text="Budget Tracker", 
                                  font=("Arial", 12, "bold"), text_color="white")
        title_label.pack()
        
        # Right side - Input fields
        fields_frame = ctk.CTkFrame(input_frame, fg_color="transparent")
        fields_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)
        
        # Create input fields
        title_label = ctk.CTkLabel(fields_frame, text="Title*", 
                                  font=("Arial", 12), text_color="white")
        title_label.grid(row=0, column=0, sticky="w", padx=5, pady=2)
        title_entry = ctk.CTkEntry(fields_frame, width=120, placeholder_text="Enter title")
        title_entry.grid(row=1, column=0, padx=5, pady=5)
        
        price_label = ctk.CTkLabel(fields_frame, text="Amount*", 
                                  font=("Arial", 12), text_color="white")
        price_label.grid(row=0, column=1, sticky="w", padx=5, pady=2)
        price_entry = ctk.CTkEntry(fields_frame, width=120, placeholder_text="Enter amount")
        price_entry.grid(row=1, column=1, padx=5, pady=5)
        
        category_label = ctk.CTkLabel(fields_frame, text="Category*", 
                                     font=("Arial", 12), text_color="white")
        category_label.grid(row=0, column=2, sticky="w", padx=5, pady=2)
        category_combobox = ctk.CTkComboBox(fields_frame, width=120,
                                           values=["Income", "Allowance", "Supermarket", "Transport", "Shopping", 
                                                  "Foods", "Drinks", "Restaurants", "Cafes", "Fast Food", "Online services",
                                                  "Housing and utilities", "Transfers to other people",
                                                  "Other"], fg_color=SECONDARY_COLOR)
        category_combobox.grid(row=1, column=2, padx=5, pady=5)
        
        comment_label = ctk.CTkLabel(fields_frame, text="Comment", 
                                    font=("Arial", 12), text_color="white")
        comment_label.grid(row=0, column=3, sticky="w", padx=5, pady=2)
        comment_entry = ctk.CTkEntry(fields_frame, width=150, placeholder_text="Enter comment")
        comment_entry.grid(row=1, column=3, padx=5, pady=5)
        
        # Required fields note
        required_label = ctk.CTkLabel(fields_frame, text="* required fields", 
                                     font=("Arial", 10), text_color="#888")
        required_label.grid(row=2, column=0, columnspan=2, sticky="w", padx=5, pady=2)
        
        # Add Record button
        add_btn = ctk.CTkButton(fields_frame, text="Add Record", 
                               fg_color="#4CAF50", hover_color="#45a049",
                               width=100, height=30, 
                               command=lambda: add_record(title_entry, price_entry, category_combobox, comment_entry))
        add_btn.grid(row=1, column=4, padx=10, pady=5)
        
        # Data table frame
        table_frame = ctk.CTkFrame(home_tab, fg_color=DARK_COLOR)
        table_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Create scrollable frame for table with improved styling
        table_scroll = ctk.CTkScrollableFrame(table_frame, height=250, fg_color=DARKEST_COLOR, 
                                            border_width=1, border_color="#666666")
        table_scroll.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Table headers with new color scheme
        headers = ["ID", "Title", "Amount", "Category", "Comment"]
        header_frame = ctk.CTkFrame(table_scroll, fg_color=SECONDARY_COLOR, 
                                   border_width=1, border_color="#666666")
        header_frame.pack(fill="x", pady=(0, 2))
        
        for i, header in enumerate(headers):
            label = ctk.CTkLabel(header_frame, text=header, font=("Arial", 12, "bold"), 
                               text_color="#FFFFFF", width=100)
            label.grid(row=0, column=i, padx=2, pady=8, sticky="ew")
        
        # Configure grid weights
        for i in range(len(headers)):
            header_frame.grid_columnconfigure(i, weight=1)
        
        # Bottom buttons frame
        buttons_frame = ctk.CTkFrame(home_tab, fg_color="transparent", height=60)
        buttons_frame.pack(fill="x", padx=10, pady=5)
        buttons_frame.pack_propagate(False)
        
        # Top row of buttons
        top_buttons = ctk.CTkFrame(buttons_frame, fg_color="transparent")
        top_buttons.pack(fill="x", pady=(0, 5))
        
        # Left side buttons
        show_all_btn = ctk.CTkButton(top_buttons, text="Show All", width=100, 
                                    fg_color=PRIMARY_COLOR, hover_color=SECONDARY_COLOR,
                                    command=load_table_data)
        show_all_btn.pack(side="left", padx=5)
        
        search_btn = ctk.CTkButton(top_buttons, text="Search", width=100,
                                  fg_color=PRIMARY_COLOR, hover_color=SECONDARY_COLOR,
                                  command=search_records)
        search_btn.pack(side="left", padx=5)
        
        # Right side button
        update_btn = ctk.CTkButton(top_buttons, text="Update Record", width=120,
                                  fg_color=PRIMARY_COLOR, hover_color=SECONDARY_COLOR,
                                  command=lambda: update_record(title_entry, price_entry, category_combobox, comment_entry))
        update_btn.pack(side="right", padx=5)
        
        # Bottom row of buttons
        bottom_buttons = ctk.CTkFrame(buttons_frame, fg_color="transparent")
        bottom_buttons.pack(fill="x")
        
        remove_selected_btn = ctk.CTkButton(bottom_buttons, text="Remove Selected Record", 
                                          fg_color="#f44336", hover_color="#da190b", 
                                          width=180, command=remove_selected_record)
        remove_selected_btn.pack(side="left", padx=5)
        
        remove_all_btn = ctk.CTkButton(bottom_buttons, text="Remove All Records", 
                                     fg_color="#f44336", hover_color="#da190b", 
                                     width=160, command=remove_all_records)
        remove_all_btn.pack(side="right", padx=5)
        
        return table_scroll, title_entry, price_entry, category_combobox, comment_entry
    
    # --- Pandas-based sorting and exporting ---
    def sort_expenses(df, column="amount", ascending=False):
        """Sort expenses DataFrame by a column."""
        return df.sort_values(by=column, ascending=ascending)

    def export_expenses(df, filename="expenses_export.csv"):
        """Export expenses DataFrame to CSV."""
        df.to_csv(filename, index=False)
        tk.messagebox.showinfo("Export", f"Data exported to {filename}")

    def filter_expenses_by_period(df, period="month"):
        """Filter expenses DataFrame by time period."""
        now = pd.Timestamp.now()
        if period == "day":
            return df[df['date'].dt.date == now.date()]
        elif period == "week":
            return df[df['date'] >= now - pd.Timedelta(days=7)]
        elif period == "month":
            return df[df['date'].dt.month == now.month]
        elif period == "quarter":
            return df[df['date'].dt.quarter == now.quarter]
        elif period == "halfyear":
            # Jan-Jun if current month <= 6, else Jul-Dec
            if now.month <= 6:
                return df[df['date'].dt.month.isin(range(1, 7))]
            else:
                return df[df['date'].dt.month.isin(range(7, 13))]
        elif period == "year":
            return df[df['date'].dt.year == now.year]
        else:
            return df

    # --- Export & Sort UI for Home Tab ---
    export_frame = ctk.CTkFrame(home_tab, fg_color="transparent")
    export_frame.pack(fill="x", padx=10, pady=(0, 10))

    ctk.CTkLabel(export_frame, text="Export Expenses:", font=("Arial", 12, "bold"), text_color="white").pack(side="left", padx=(0,10))

    # Dropdown for period selection
    export_periods = ["Day", "Week", "Month", "Quarter", "Half-Year", "Year"]
    export_dropdown = ctk.CTkComboBox(export_frame, values=export_periods, width=120)
    export_dropdown.set("Month")  # Default
    export_dropdown.pack(side="left", padx=2)

    # Export button
    def export_selected_period():
        period = export_dropdown.get().lower().replace("-", "").replace(" ", "")
        df = fetch_expense_data(userid)
        filtered = filter_expenses_by_period(df, period)
        export_expenses(filtered, f"expenses_{period}.csv")
    ctk.CTkButton(export_frame, text="Export", command=export_selected_period, width=90).pack(side="left", padx=10)

    # Download CSV of current table
    def download_table_csv():
        df = fetch_expense_data(userid)
        export_expenses(df, "expenses_table.csv")
    ctk.CTkButton(export_frame, text="Download CSV", command=download_table_csv, width=120).pack(side="left", padx=10)
    
    # ==================== GRAPH TAB ====================
    def setup_graph_tab():
        # Configure the tab background
        graph_tab.configure(fg_color=DARKER_COLOR)
        
        # Create main container for the graph tab
        main_container = ctk.CTkFrame(graph_tab, fg_color="transparent")
        main_container.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Financial Summary at the top
        summary_frame = ctk.CTkFrame(main_container, height=120, fg_color=DARK_COLOR)
        summary_frame.pack(fill="x", padx=20, pady=(0, 15))
        summary_frame.pack_propagate(False)

        # Title
        summary_title = ctk.CTkLabel(summary_frame, text="💰 Financial Summary", 
                                    font=("Arial", 18, "bold"), text_color="white")
        summary_title.pack(pady=(10, 0))

        # Card container for summary cards
        card_container = ctk.CTkFrame(summary_frame, fg_color="transparent")
        card_container.pack(fill="x", expand=True, padx=10, pady=10)

        # Each card (even gaps, fills container)
        income_card = ctk.CTkFrame(card_container, fg_color=DARKER_COLOR)
        income_card.pack(side="left", fill="both", expand=True, padx=10)
        expense_card = ctk.CTkFrame(card_container, fg_color=DARKER_COLOR)
        expense_card.pack(side="left", fill="both", expand=True, padx=10)
        calc_card = ctk.CTkFrame(card_container, fg_color=DARKER_COLOR)
        calc_card.pack(side="left", fill="both", expand=True, padx=10)
        balance_card = ctk.CTkFrame(card_container, fg_color=DARKER_COLOR)
        balance_card.pack(side="left", fill="both", expand=True, padx=10)

        # Income Card
        income_title = ctk.CTkLabel(income_card, text="💵 Total Income + Allowance", 
                                    font=("Arial", 11, "bold"), text_color="#2ECC71")
        income_title.pack(pady=(8, 3))
        global income_label
        income_label = ctk.CTkLabel(income_card, text="₱0.00", 
                                    font=("Arial", 14, "bold"), text_color="white")
        income_label.pack(pady=(0, 8))

        # Expense Card
        expense_title = ctk.CTkLabel(expense_card, text="💸 Total Expenses", 
                                    font=("Arial", 11, "bold"), text_color="#E74C3C")
        expense_title.pack(pady=(8, 3))
        global expense_label
        expense_label = ctk.CTkLabel(expense_card, text="₱0.00", 
                                    font=("Arial", 14, "bold"), text_color="white")
        expense_label.pack(pady=(0, 8))

        # Calculation Card
        calc_title = ctk.CTkLabel(calc_card, text="🧮 Calculation", 
                                font=("Arial", 11, "bold"), text_color="#F39C12")
        calc_title.pack(pady=(8, 3))
        global calculation_label
        calculation_label = ctk.CTkLabel(calc_card, text="₱0.00 - ₱0.00 = ₱0.00", 
                                        font=("Arial", 12, "bold"), text_color="white")
        calculation_label.pack(pady=(0, 8))

        # Balance Card
        balance_title = ctk.CTkLabel(balance_card, text="💳 Available Balance", 
                                    font=("Arial", 11, "bold"), text_color="#9B59B6")
        balance_title.pack(pady=(8, 3))
        global balance_label
        balance_label = ctk.CTkLabel(balance_card, text="₱0.00", 
                                    font=("Arial", 14, "bold"), text_color="white")
        balance_label.pack(pady=(0, 8))
        
        # Chart section (replace CTkFrame with CTkScrollableFrame)
        chart_container = ctk.CTkScrollableFrame(main_container, fg_color=DARK_COLOR)
        chart_container.pack(fill="both", expand=True)
        # Chart title
        title_label = ctk.CTkLabel(chart_container, text="📊 Expense Distribution", 
                                font=("Arial", 16, "bold"), text_color="white")
        title_label.pack(pady=(20, 10))
        return chart_container, summary_frame
    
    def calculate_balance():
        """Calculate and update financial summary with calculation display"""
        cur = conn.cursor()
        
        try:
            # Calculate total income (Income + Allowance)
            cur.execute("SELECT SUM(amount) FROM expense WHERE userid = %s AND expense_type IN ('Income', 'Allowance')", (userid,))
            result = cur.fetchone()
            total_income = float(result[0]) if result[0] is not None else 0.0
            
            # Calculate total expenses (everything except Income and Allowance)
            cur.execute("SELECT SUM(amount) FROM expense WHERE userid = %s AND expense_type NOT IN ('Income', 'Allowance')", (userid,))
            result = cur.fetchone()
            total_expenses = float(result[0]) if result[0] is not None else 0.0
            
            # Calculate balance
            balance = total_income - total_expenses
            
            # Update labels with peso symbol
            income_label.configure(text=f"₱{total_income:,.2f}")
            expense_label.configure(text=f"₱{total_expenses:,.2f}")
            
            # Update calculation display
            calculation_label.configure(text=f"₱{total_income:,.2f} - ₱{total_expenses:,.2f} = ₱{balance:,.2f}")
            
            # Color balance based on positive/negative
            balance_color = "#2ECC71" if balance >= 0 else "#E74C3C"
            balance_label.configure(text=f"₱{balance:,.2f}", text_color=balance_color)
            
            return total_income, total_expenses, balance
            
        except Exception as e:
            print(f"Error calculating balance: {e}")
            income_label.configure(text="₱0.00")
            expense_label.configure(text="₱0.00")
            calculation_label.configure(text="₱0.00 - ₱0.00 = ₱0.00")
            balance_label.configure(text="₱0.00")
            return 0, 0, 0
    
    def add_record(title_entry, price_entry, category_combobox, comment_entry):
        """Add a new record to the database"""
        try:
            title = title_entry.get().strip()
            price = price_entry.get().strip()
            category = category_combobox.get()
            comment = comment_entry.get().strip()
            
            if not all([title, price, category]):
                tk.messagebox.showerror("Error", "Please fill in all required fields")
                return
            
            amount = float(price)
            if amount <= 0:
                tk.messagebox.showerror("Error", "Amount must be greater than 0")
                return
            
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO expense (userid, date, title, expense_type, amount, comment) VALUES (%s, %s, %s, %s, %s, %s)",
                (userid, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), title, category, amount, comment),
            )
            conn.commit()
            
            # Clear entries
            title_entry.delete(0, ctk.END)
            price_entry.delete(0, ctk.END)
            category_combobox.set("")
            comment_entry.delete(0, ctk.END)
            
            load_table_data()
            update_chart()
            calculate_balance()
            
            if category in ['Income', 'Allowance']:
                tk.messagebox.showinfo("Success", f"{category} of ₱{amount:,.2f} added successfully!")
            else:
                tk.messagebox.showinfo("Success", f"Expense of ₱{amount:,.2f} added successfully!")
            
        except ValueError:
            tk.messagebox.showerror("Error", "Please enter a valid amount (numbers only)")
        except Exception as e:
            tk.messagebox.showerror("Error", f"Database error: {str(e)}")
    
    def load_table_data():
        """Load data into the table with new color scheme"""
        nonlocal table_data
        # Clear existing data
        for widget in table_scroll.winfo_children()[1:]:  # Keep header
            widget.destroy()
        
        cur = conn.cursor()
        try:
            cur.execute("SELECT id, title, expense_type, amount, comment FROM expense WHERE userid = %s ORDER BY id DESC LIMIT 20", (userid,))
            rows = cur.fetchall()
            table_data = rows
            
            for i, row in enumerate(rows):
                # Alternating row colors: even = DARK_COLOR, odd = DARKER_COLOR
                row_bg_color = DARK_COLOR if i % 2 == 0 else DARKER_COLOR
                
                row_frame = ctk.CTkFrame(table_scroll, fg_color=row_bg_color, 
                                       border_width=1, border_color="#666666")
                row_frame.pack(fill="x", pady=1)
                
                # Make row clickable
                def on_row_click(record_id=row[0], row_index=i):
                    nonlocal selected_record_id
                    selected_record_id = record_id
                    # Highlight selected row with PRIMARY_COLOR
                    for j, widget in enumerate(table_scroll.winfo_children()[1:]):
                        if j == row_index:
                            widget.configure(fg_color=PRIMARY_COLOR)
                            # Update all labels in the selected row to white text
                            for child in widget.winfo_children():
                                if isinstance(child, ctk.CTkLabel):
                                    if "Amount" not in child.cget("text") or (j == row_index and "₱" in child.cget("text")):
                                        # Keep amount color coding but ensure visibility
                                        if "₱" in child.cget("text"):
                                            if row[2] in ['Income', 'Allowance']:
                                                child.configure(text_color="#2ECC71")
                                            else:
                                                child.configure(text_color="#E74C3C")
                                        else:
                                            child.configure(text_color="#FFFFFF")
                        else:
                            # Reset to alternating colors
                            original_bg = DARK_COLOR if j % 2 == 0 else DARKER_COLOR
                            widget.configure(fg_color=original_bg)
                            # Reset text colors
                            for child in widget.winfo_children():
                                if isinstance(child, ctk.CTkLabel):
                                    child.configure(text_color="#FFFFFF")
                
                row_frame.bind("<Button-1>", lambda e, record_id=row[0], row_index=i: on_row_click(record_id, row_index))
                
                # Display: ID, Title, Amount, Category, Comment
                # Color coding for income vs expenses (only for amount column)
                amount_color = "#FFFFFF"  
                if row[2] in ['Income', 'Allowance']:
                    amount_display = f"+₱{row[3]:,.2f}"
                    amount_color = "#2ECC71"  # Green for income
                else:
                    amount_display = f"-₱{row[3]:,.2f}"
                    amount_color = "#E74C3C"  # Red for expenses
                
                data = [str(row[0]), row[1][:20] + "..." if len(row[1]) > 20 else row[1], 
                       amount_display, row[2], (row[4] or "No comment")[:15] + "..." if row[4] and len(row[4]) > 15 else (row[4] or "No comment")]
                
                for j, value in enumerate(data):
                    if j == 2:  # Amount column
                        label = ctk.CTkLabel(row_frame, text=value, font=("Arial", 10, "bold"), 
                                           text_color=amount_color, width=100)
                    else:
                        label = ctk.CTkLabel(row_frame, text=value, font=("Arial", 10), 
                                           text_color="#FFFFFF", width=100)  # White text for all other columns
                    label.grid(row=0, column=j, padx=2, pady=6, sticky="ew")
                    label.bind("<Button-1>", lambda e, record_id=row[0], row_index=i: on_row_click(record_id, row_index))
                
                # Configure grid weights
                for j in range(len(data)):
                    row_frame.grid_columnconfigure(j, weight=1)
        except Exception as e:
            print(f"Error loading table data: {e}")
    
    def search_records():
        """Search functionality"""
        search_window = ctk.CTkToplevel(app)
        search_window.title("Search Records")
        search_window.geometry("400x200")
        search_window.configure(fg_color=DARKER_COLOR)
        
        search_label = ctk.CTkLabel(search_window, text="Search by title, category, or comment:", 
                                   font=("Arial", 14), text_color="white")
        search_label.pack(pady=20)
        
        search_entry = ctk.CTkEntry(search_window, width=300, placeholder_text="Enter search term")
        search_entry.pack(pady=10)
        
        def perform_search():
            search_term = search_entry.get().strip()
            if search_term:
                # Clear existing data
                for widget in table_scroll.winfo_children()[1:]:
                    widget.destroy()
                
                cur = conn.cursor()
                cur.execute(
                    "SELECT id, title, expense_type, amount, comment FROM expense WHERE userid = %s AND (expense_type LIKE %s OR comment LIKE %s OR title LIKE %s) ORDER BY id DESC",
                    (userid, f"%{search_term}%", f"%{search_term}%", f"%{search_term}%")
                )
                rows = cur.fetchall()
                
                for i, row in enumerate(rows):
                    # Alternating row colors
                    row_bg_color = DARK_COLOR if i % 2 == 0 else DARKER_COLOR
                    
                    row_frame = ctk.CTkFrame(table_scroll, fg_color=row_bg_color,
                                           border_width=1, border_color="#666666")
                    row_frame.pack(fill="x", pady=1)
                    
                    # Color coding for amount
                    if row[2] in ['Income', 'Allowance']:
                        amount_display = f"+₱{row[3]:,.2f}"
                        amount_color = "#2ECC71"
                    else:
                        amount_display = f"-₱{row[3]:,.2f}"
                        amount_color = "#E74C3C"
                    
                    data = [str(row[0]), row[1][:20] + "..." if len(row[1]) > 20 else row[1], 
                           amount_display, row[2], (row[4] or "")[:15] + "..." if row[4] and len(row[4]) > 15 else (row[4] or "")]
                    
                    for j, value in enumerate(data):
                        if j == 2:  # Amount column
                            label = ctk.CTkLabel(row_frame, text=value, font=("Arial", 10, "bold"), 
                                               text_color=amount_color, width=100)
                        else:
                            label = ctk.CTkLabel(row_frame, text=value, font=("Arial", 10), 
                                               text_color="#FFFFFF", width=100)
                        label.grid(row=0, column=j, padx=2, pady=6, sticky="ew")
                    
                    for j in range(len(data)):
                        row_frame.grid_columnconfigure(j, weight=1)
                
                search_window.destroy()
        
        search_btn = ctk.CTkButton(search_window, text="Search", command=perform_search,
                                  fg_color=PRIMARY_COLOR, hover_color=SECONDARY_COLOR)
        search_btn.pack(pady=20)
    
    def update_record(title_entry, price_entry, category_combobox, comment_entry):
        """Update selected record"""
        if not selected_record_id:
            tk.messagebox.showerror("Error", "Please select a record to update")
            return
        
        title = title_entry.get().strip()
        price = price_entry.get().strip()
        category = category_combobox.get()
        comment = comment_entry.get().strip()
        
        if not all([title, price, category]):
            tk.messagebox.showerror("Error", "Please fill in all required fields")
            return
        
        try:
            amount = float(price)
            if amount <= 0:
                tk.messagebox.showerror("Error", "Amount must be greater than 0")
                return
                
            cur = conn.cursor()
            cur.execute(
                "UPDATE expense SET title = %s, expense_type = %s, amount = %s, comment = %s WHERE id = %s",
                (title, category, amount, comment, selected_record_id)
            )
            conn.commit()
            
            # Clear entries
            title_entry.delete(0, ctk.END)
            price_entry.delete(0, ctk.END)
            category_combobox.set("")
            comment_entry.delete(0, ctk.END)
            
            load_table_data()
            update_chart()
            calculate_balance()
            tk.messagebox.showinfo("Success", "Record updated successfully!")
            
        except ValueError:
            tk.messagebox.showerror("Error", "Please enter a valid amount (numbers only)")
        except Exception as e:
            tk.messagebox.showerror("Error", f"Database error: {str(e)}")
    
    def remove_selected_record():
        """Remove selected record"""
        if not selected_record_id:
            tk.messagebox.showerror("Error", "Please select a record to remove")
            return
        
        if tk.messagebox.askyesno("Confirm", "Are you sure you want to remove this record?"):
            try:
                cur = conn.cursor()
                cur.execute("DELETE FROM expense WHERE id = %s", (selected_record_id,))
                conn.commit()
                
                load_table_data()
                update_chart()
                calculate_balance()
                tk.messagebox.showinfo("Success", "Record removed successfully!")
                
            except Exception as e:
                tk.messagebox.showerror("Error", f"Database error: {str(e)}")
    
    def remove_all_records():
        """Remove all records for user"""
        if tk.messagebox.askyesno("Confirm", "Are you sure you want to remove ALL records? This cannot be undone!"):
            try:
                cur = conn.cursor()
                cur.execute("DELETE FROM expense WHERE userid = %s", (userid,))
                conn.commit()
                
                load_table_data()
                update_chart()
                calculate_balance()
                tk.messagebox.showinfo("Success", "All records removed successfully!")
                
            except Exception as e:
                tk.messagebox.showerror("Error", f"Database error: {str(e)}")
    
    def update_chart():
        """Update the pie chart and line graph for expense distribution and balance trend, with sorting controls."""
        # Clear existing chart except the title
        for widget in chart_frame.winfo_children()[1:]:
            widget.destroy()

        cur = conn.cursor()
        try:
            # --- PIE CHART: Expense Distribution ---
            cur.execute(
                "SELECT expense_type, SUM(amount) FROM expense WHERE userid = %s AND expense_type NOT IN ('Income', 'Allowance') GROUP BY expense_type",
                (userid,))
            data = cur.fetchall()

            labels = []
            sizes = []
            colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FECA57',
                    '#A569BD', '#F39C12', '#E74C3C', '#3498DB', '#2ECC71']

            if data:
                for i, (category, amount) in enumerate(data):
                    labels.append(category)
                    sizes.append(float(amount))

                if len(labels) > len(colors):
                    import itertools
                    colors = list(itertools.islice(itertools.cycle(colors), len(labels)))

                # Main horizontal frame for split layout
                split_frame = ctk.CTkFrame(chart_frame, fg_color=DARKER_COLOR)
                split_frame.pack(fill="both", expand=True, padx=20, pady=20)

                # Left frame: Pie chart (70%)
                left_frame = ctk.CTkFrame(split_frame, fg_color=DARK_COLOR, width=700)
                left_frame.pack(side="left", fill="both", expand=True)
                left_frame.pack_propagate(False)

                # Right frame: Legend (30%)
                right_frame = ctk.CTkFrame(split_frame, fg_color=DARK_COLOR, width=300)
                right_frame.pack(side="right", fill="y")
                right_frame.pack_propagate(False)

                # Pie chart (no legend inside chart)
                fig, ax = plt.subplots(figsize=(10, 10), facecolor=DARK_COLOR)
                ax.set_facecolor(DARK_COLOR)
                wedges, texts = ax.pie(
                    sizes,
                    labels=None,
                    colors=colors[:len(labels)],
                    autopct=None,
                    startangle=90,
                    shadow=True,
                    explode=[0.05] * len(labels),
                    wedgeprops={'linewidth': 2, 'edgecolor': 'white'}
                )
                ax.set_title("", pad=0)
                plt.tight_layout()

                canvas = FigureCanvasTkAgg(fig, master=left_frame)
                canvas.draw()
                canvas.get_tk_widget().pack(expand=True, fill="both", padx=10, pady=10)

                # --- Tooltip for Pie Chart ---
                tooltip = tk.Label(left_frame, bg="#222", fg="white", font=("Arial", 11), bd=1, relief="solid")
                tooltip.place_forget()

                def on_motion(event):
                    found = False
                    for i, wedge in enumerate(wedges):
                        if wedge.contains_point([event.x, event.y]):
                            tooltip.config(text=f"{labels[i]}: ₱{sizes[i]:,.2f}")
                            tooltip.place(x=event.x + 10, y=event.y + 10)
                            found = True
                            break
                    if not found:
                        tooltip.place_forget()

                canvas.mpl_connect("motion_notify_event", on_motion)

                # Legend on right frame (all visible, scrollable if needed)
                legend_title = ctk.CTkLabel(right_frame, text="Expense Categories", font=("Arial", 14, "bold"), text_color="white")
                legend_title.pack(pady=(20, 10))

                legend_scroll = ctk.CTkScrollableFrame(right_frame, fg_color=DARK_COLOR, width=280, height=300)
                legend_scroll.pack(fill="both", expand=True, padx=10, pady=10)

                for i, (label, size) in enumerate(zip(labels, sizes)):
                    row = ctk.CTkFrame(legend_scroll, fg_color="transparent")
                    row.pack(fill="x", pady=4)
                    color_box = ctk.CTkLabel(row, text="", width=20, height=20, fg_color=colors[i])
                    color_box.pack(side="left", padx=(0, 8))
                    legend_label = ctk.CTkLabel(
                        row,
                        text=f"{label}: ₱{size:,.0f}",
                        font=("Arial", 12),
                        text_color="white",
                        anchor="w"
                    )
                    legend_label.pack(side="left", fill="x", expand=True)
            else:
                no_data_label = ctk.CTkLabel(chart_frame, text="No expense data available\nAdd some expenses to see the chart",
                                            font=("Arial", 16), text_color="white")
                no_data_label.pack(expand=True)

            # --- BALANCE TREND SORT CONTROLS ---
            sort_frame = ctk.CTkFrame(chart_frame, fg_color="transparent")
            sort_frame.pack(fill="x", padx=20, pady=(0, 0))

            ctk.CTkLabel(sort_frame, text="Sort Balance Trend by:", font=("Arial", 12, "bold"), text_color="white").pack(side="left", padx=(0,10))

            trend_periods = ["Day", "Week", "Month", "Year"]
            trend_dropdown = ctk.CTkComboBox(sort_frame, values=trend_periods, width=120)
            trend_dropdown.set("Month")
            trend_dropdown.pack(side="left", padx=2)

            # --- Dedicated container for balance trend chart ---
            balance_trend_container = ctk.CTkFrame(chart_frame, fg_color="transparent")
            balance_trend_container.pack(fill="x", padx=0, pady=(0, 0))

            def filter_balance_trend(records, period):
                df = pd.DataFrame(records, columns=["date", "amount", "expense_type"])
                df["date"] = pd.to_datetime(df["date"])
                now = pd.Timestamp.now()
                if period == "Day":
                    df = df[df["date"].dt.date == now.date()]
                elif period == "Week":
                    df = df[df["date"] >= now - pd.Timedelta(days=7)]
                elif period == "Month":
                    df = df[df["date"].dt.month == now.month]
                elif period == "Year":
                    df = df[df["date"].dt.year == now.year]
                return df.values.tolist()

            def draw_balance_trend(records):
                # Clear previous chart in container
                for widget in balance_trend_container.winfo_children():
                    widget.destroy()

                # Create a dedicated frame for the line chart (always)
                balance_trend_frame = ctk.CTkFrame(balance_trend_container, fg_color=DARK_COLOR)
                balance_trend_frame.pack(fill="x", padx=20, pady=(0, 10))

                # Centered header (always)
                balance_header = ctk.CTkLabel(balance_trend_frame, text="📈 Balance Trend", font=("Arial", 18, "bold"), text_color="white")
                balance_header.pack(pady=(10, 0), fill="x")

                if records:
                    dates = []
                    balances = []
                    total = 0.0
                    for row in records:
                        dt = pd.to_datetime(row[0])
                        amount = float(row[1])
                        if row[2] in ('Income', 'Allowance'):
                            total += amount
                        else:
                            total -= amount
                        dates.append(dt)
                        balances.append(total)

                    fig2, ax2 = plt.subplots(figsize=(7, 3), facecolor=DARK_COLOR)
                    ax2.set_facecolor(DARK_COLOR)
                    ax2.plot(
                        dates,
                        balances,
                        marker='o',
                        markersize=8,
                        markerfacecolor='#39ace7',
                        markeredgecolor='white',
                        color='#39ace7',
                        linewidth=2,
                        label='Balance'
                    )
                    ax2.axhline(0, color='#E74C3C', linestyle='--', linewidth=2, label='Limit (₱0)')
                    ax2.set_title("", pad=0)
                    ax2.set_ylabel("Balance (₱)", color='white')
                    ax2.set_xlabel("Date", color='white')
                    ax2.tick_params(axis='x', labelrotation=45, colors='white')
                    ax2.tick_params(axis='y', colors='white')
                    ax2.legend(facecolor=DARK_COLOR, edgecolor='white', fontsize=10)
                    ax2.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
                    ax2.xaxis.set_major_locator(mdates.AutoDateLocator())
                    fig2.autofmt_xdate()
                    fig2.tight_layout()

                    canvas2 = FigureCanvasTkAgg(fig2, master=balance_trend_frame)
                    canvas2.draw()
                    canvas2.get_tk_widget().pack(expand=True, fill="both", padx=10, pady=10)

                    # Add interactive toolbar below the line graph
                    toolbar = NavigationToolbar2Tk(canvas2, balance_trend_frame)
                    toolbar.update()
                    toolbar.pack(fill="x", padx=10, pady=(0, 10))

                    # --- Tooltip for Line Graph ---
                    tooltip_line = tk.Label(balance_trend_frame, bg="#222", fg="white", font=("Arial", 11), bd=1, relief="solid")
                    tooltip_line.place_forget()

                    def on_line_motion(event):
                        found = False
                        if event.inaxes == ax2:
                            mouse_x, mouse_y = event.xdata, event.ydata
                            if mouse_x is not None and mouse_y is not None:
                                for i, (x, y) in enumerate(zip(dates, balances)):
                                    x_val = ax2.transData.transform((mdates.date2num(x), float(y)))
                                    mouse_val = (event.x, event.y)
                                    dist = ((x_val[0] - mouse_val[0]) ** 2 + (x_val[1] - mouse_val[1]) ** 2) ** 0.5
                                    if dist < 20:
                                        tooltip_line.config(text=f"{x.strftime('%Y-%m-%d')}: ₱{y:,.2f}")
                                        tooltip_line.place(x=event.x + 10, y=event.y + 10)
                                        found = True
                                        break
                        if not found:
                            tooltip_line.place_forget()

                    canvas2.mpl_connect("motion_notify_event", on_line_motion)

                else:
                    # Show "No data" message but keep header and controls
                    no_data_label2 = ctk.CTkLabel(balance_trend_frame, text="No balance trend data available.",
                                                font=("Arial", 12), text_color="white")
                    no_data_label2.pack(pady=30)

            def refresh_balance_trend():
                selected_period = trend_dropdown.get()
                cur = conn.cursor()
                cur.execute("""
                    SELECT date, amount, expense_type
                    FROM expense
                    WHERE userid = %s
                    ORDER BY date ASC, id ASC
                """, (userid,))
                all_records = cur.fetchall()
                filtered_records = filter_balance_trend(all_records, selected_period)
                draw_balance_trend(filtered_records)

            sort_btn = ctk.CTkButton(sort_frame, text="Sort", command=refresh_balance_trend, width=80, fg_color=PRIMARY_COLOR, hover_color=SECONDARY_COLOR)
            sort_btn.pack(side="left", padx=10)

            # Initial draw with all records (default period)
            cur.execute("""
                SELECT date, amount, expense_type
                FROM expense
                WHERE userid = %s
                ORDER BY date ASC, id ASC
            """, (userid,))
            all_records = cur.fetchall()
            filtered_records = filter_balance_trend(all_records, trend_dropdown.get())
            draw_balance_trend(filtered_records)

        except Exception as e:
            error_label = ctk.CTkLabel(chart_frame, text=f"Error loading chart: {str(e)}",
                                    font=("Arial", 16), text_color="#E74C3C")
            error_label.pack(expand=True)
    
    # Setup tabs
    table_scroll, title_entry, price_entry, category_combobox, comment_entry = setup_home_tab()
    chart_frame, balance_frame = setup_graph_tab()
    
    # Load initial data
    load_table_data()
    update_chart()
    calculate_balance()

def signUp_page():
    clear_window()
    
    def go_first_page():
        first_page()
        
    def submit():
        get_userid = userid_entry.get().strip()
        get_name = name_entry.get().strip()
        get_password = password_entry.get().strip()

        if not get_userid or not get_name or not get_password:
            tk.messagebox.showerror("Error", "Please fill in all fields")
            return

        cur = conn.cursor()
        try:
            cur.execute("SELECT userid FROM userinfo WHERE userid = %s", (get_userid,))
            if cur.fetchone():
                tk.messagebox.showerror("Sign Up", "User ID is already taken")
                return
                
            cur.execute(
                "INSERT INTO userinfo (userid, password, user_name) VALUES (%s, %s, %s)",
                (get_userid, get_password, get_name),
            )
            conn.commit()
            tk.messagebox.showinfo("Success", "Account created successfully!")
            second_page(get_userid)
        except Exception as e:
            tk.messagebox.showerror("Sign Up Error", str(e))

    # Main container
    main_frame = ctk.CTkFrame(app, fg_color=PRIMARY_COLOR)
    main_frame.pack(fill="both", expand=True)
    
    # Left side - Welcome text
    left_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
    left_frame.pack(side="left", fill="both", expand=True, padx=50, pady=50)
    
    welcome_label = ctk.CTkLabel(left_frame, 
                                text="Join Our\nBudget Tracker\nCommunity", 
                                font=("Arial", 36, "bold"), 
                                text_color="white")
    welcome_label.pack(expand=True)
    
    subtitle_label = ctk.CTkLabel(left_frame, 
                                 text="Take control of your finances and\nunlock your financial freedom", 
                                 font=("Arial", 16), 
                                 text_color="white")
    subtitle_label.pack(pady=(20, 0))
    
    # Right side - Sign up form
    right_frame = ctk.CTkFrame(main_frame, width=400, fg_color="white", corner_radius=20)
    right_frame.pack(side="right", fill="y", padx=50, pady=50)
    right_frame.pack_propagate(False)
    
    # Form content
    form_frame = ctk.CTkFrame(right_frame, fg_color="transparent")
    form_frame.pack(expand=True, fill="both", padx=40, pady=40)
    
    title_label = ctk.CTkLabel(form_frame, text="Create Account", 
                              font=("Arial", 24, "bold"), text_color=DARKEST_COLOR)
    title_label.pack(pady=(0, 30))
    
    # Username field
    username_label = ctk.CTkLabel(form_frame, text="Username", 
                                 font=("Arial", 14), text_color=DARKEST_COLOR)
    username_label.pack(anchor="w")
    userid_entry = ctk.CTkEntry(form_frame, width=320, height=40, 
                               placeholder_text="Enter username")
    userid_entry.pack(pady=(5, 20))
    
    # Name field
    name_label = ctk.CTkLabel(form_frame, text="Full Name", 
                             font=("Arial", 14), text_color=DARKEST_COLOR)
    name_label.pack(anchor="w")
    name_entry = ctk.CTkEntry(form_frame, width=320, height=40, 
                             placeholder_text="Enter your full name")
    name_entry.pack(pady=(5, 20))
    
    # Password field
    password_label = ctk.CTkLabel(form_frame, text="Password", 
                                 font=("Arial", 14), text_color=DARKEST_COLOR)
    password_label.pack(anchor="w")
    password_entry = ctk.CTkEntry(form_frame, width=320, height=40, 
                                 placeholder_text="Enter password", show="*")
    password_entry.pack(pady=(5, 30))
    
    # Buttons
    signup_btn = ctk.CTkButton(form_frame, text="Create Account", command=submit,
                              width=320, height=40, fg_color=SECONDARY_COLOR, 
                              hover_color=PRIMARY_COLOR, font=("Arial", 14, "bold"))
    signup_btn.pack(pady=(0, 15))
    
    login_btn = ctk.CTkButton(form_frame, text="Already have an account? Login", 
                             command=go_first_page, width=320, height=40, 
                             fg_color="transparent", text_color=SECONDARY_COLOR, 
                             hover_color="#ECF0F1", border_width=2, border_color=SECONDARY_COLOR)
    login_btn.pack()

def first_page():
    clear_window()
    
    def submit():
        get_userid = entry1.get().strip()
        get_password = entry2.get().strip()

        if not get_userid or not get_password:
            tk.messagebox.showerror("Error", "Please fill in all fields")
            return

        cur = conn.cursor()
        try:
            # First check if user exists
            cur.execute("SELECT userid FROM userinfo WHERE userid = %s", (get_userid,))
            user_exists = cur.fetchone()
            
            if not user_exists:
                # User doesn't exist in database
                result = tk.messagebox.askyesno("User Not Found", 
                                              "User isn't found. Would you like to create an account?")
                if result:
                    signUp_page()
                return
            
            # User exists, now check password
            cur.execute("SELECT userid, password FROM userinfo WHERE userid = %s AND password = %s", 
                       (get_userid, get_password))
            user = cur.fetchone()
            
            if user:
                second_page(get_userid)
            else:
                tk.messagebox.showerror("Login Error", "Invalid password. Please try again.")
                
        except Exception as e:
            tk.messagebox.showerror("Database Error", str(e))

    def signUp_page_call():
        signUp_page()

    # Main container
    main_frame = ctk.CTkFrame(app, fg_color=DARKER_COLOR)
    main_frame.pack(fill="both", expand=True)
    
    # Left side - Welcome text
    left_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
    left_frame.pack(side="left", fill="both", expand=True, padx=50, pady=50)
    
    welcome_label = ctk.CTkLabel(left_frame, 
                                text="Welcome to\nXpense", 
                                font=("Arial", 36, "bold"), 
                                text_color="white")
    welcome_label.pack(expand=True)
    
    subtitle_label = ctk.CTkLabel(left_frame, 
                                 text="Take control of your expenses and\nunlock financial freedom", 
                                 font=("Arial", 16), 
                                 text_color="white")
    subtitle_label.pack(pady=(20, 0))
    
    # Right side - Login form
    right_frame = ctk.CTkFrame(main_frame, width=400, fg_color="white", corner_radius=20)
    right_frame.pack(side="right", fill="y", padx=50, pady=50)
    right_frame.pack_propagate(False)
    
    # Form content
    form_frame = ctk.CTkFrame(right_frame, fg_color="transparent")
    form_frame.pack(expand=True, fill="both", padx=40, pady=40)
    
    title_label = ctk.CTkLabel(form_frame, text="Login", 
                              font=("Arial", 24, "bold"), text_color=DARKEST_COLOR)
    title_label.pack(pady=(0, 30))
    
    # Username field
    username_label = ctk.CTkLabel(form_frame, text="Username", 
                                 font=("Arial", 14), text_color=DARKEST_COLOR)
    username_label.pack(anchor="w")
    entry1 = ctk.CTkEntry(form_frame, width=320, height=40, 
                         placeholder_text="Enter username")
    entry1.pack(pady=(5, 20))
    
    # Password field
    password_label = ctk.CTkLabel(form_frame, text="Password", 
                                 font=("Arial", 14), text_color=DARKEST_COLOR)
    password_label.pack(anchor="w")
    entry2 = ctk.CTkEntry(form_frame, width=320, height=40, 
                         placeholder_text="Enter password", show="*")
    entry2.pack(pady=(5, 30))
    
    # Buttons
    login_btn = ctk.CTkButton(form_frame, text="Login", command=submit,
                             width=320, height=40, fg_color=PRIMARY_COLOR, 
                             hover_color=SECONDARY_COLOR, font=("Arial", 14, "bold"))
    login_btn.pack(pady=(0, 15))
    
    signup_btn = ctk.CTkButton(form_frame, text="Create New Account", 
                              command=signUp_page_call, width=320, height=40, 
                              fg_color="transparent", text_color=SECONDARY_COLOR, 
                              hover_color="#ECF0F1", border_width=2, border_color=SECONDARY_COLOR)
    signup_btn.pack()

# Start the application
if __name__ == "__main__":
    try:
        first_page()
        app.protocol("WM_DELETE_WINDOW", app.quit)  # Graceful exit
        app.mainloop()
    except (KeyboardInterrupt, tk.TclError):
        pass