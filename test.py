import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

df = pd.read_csv("salesmen.csv")
df["Date"] = pd.to_datetime(df["Date"])

salesman_colors = {
    'Alexander': '#FF6B6B',
    'Dave': '#4ECDC4', 
    'Oscar': '#45B7D1',
    'Ronald': '#96CEB4',
    'Sharon': '#FFEAA7'
}

def annotate_bars(ax):
    for p in ax.patches:
        ax.annotate(f'{int(p.get_height()):,}', 
                    (p.get_x() + p.get_width() / 2, p.get_height()), 
                    ha='center', va='bottom', fontsize=9, color='black')

def plot_general_overview(perf):
    # Sort by Total_Revenue ascending
    perf_sorted = perf.sort_values("Total_Revenue", ascending=True)
    fig, ax = plt.subplots()
    total_revenue = perf_sorted["Total_Revenue"]
    colors = [salesman_colors[salesman] for salesman in total_revenue.index]
    bars = ax.bar(total_revenue.index, total_revenue.values, color=colors)
    for bar in bars:
        ax.annotate(f'{int(bar.get_height()):,}', 
                    (bar.get_x() + bar.get_width() / 2, bar.get_height()), 
                    ha='center', va='bottom', fontsize=10, color='black')
    ax.set_title("Total Revenue per Salesman (2025)")
    ax.set_ylabel("Total Revenue")
    ax.set_xlabel("Salesman")
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, p: f'{int(x):,}'))
    fig.tight_layout()
    return fig

def plot_performance_table(perf):
    fig, ax = plt.subplots(figsize=(8, 2))
    ax.axis('off')
    table_data = perf.reset_index()
    table = ax.table(
        cellText=table_data.values,
        colLabels=table_data.columns,
        cellLoc='center',
        loc='center'
    )
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.auto_set_column_width(col=list(range(len(table_data.columns))))
    plt.title("Salesmen Performance Table (2025)", pad=20)
    fig.tight_layout()
    return fig

def plot_weekly_revenue(weekly_revenue):
    # Sort by revenue ascending
    weekly_revenue_sorted = weekly_revenue.sort_values(ascending=True)
    fig, ax = plt.subplots()
    colors = [salesman_colors[salesman] for salesman in weekly_revenue_sorted.index]
    bars = ax.bar(weekly_revenue_sorted.index, weekly_revenue_sorted.values, color=colors)
    annotate_bars(ax)
    ax.set_title("Total Revenue per Salesman (Week of July 14–20, 2025)")
    ax.set_ylabel("Revenue (Amount)")
    ax.set_xlabel("Salesman")
    fig.tight_layout()
    return fig

def plot_sharon_june(sharon_june):
    fig, ax = plt.subplots()
    ax.plot(sharon_june["Date"], sharon_june["Revenue"], marker="o", label="Daily Revenue", color=salesman_colors['Sharon'])
    for i, v in enumerate(sharon_june["Revenue"]):
        ax.annotate(f'{int(v)}', (sharon_june["Date"].iloc[i], v), ha='center', va='bottom', fontsize=9, color='black')
    ax.axhline(sharon_june["Revenue"].max(), color="green", linestyle="--", label="Max")
    ax.axhline(sharon_june["Revenue"].min(), color="red", linestyle="--", label="Min")
    ax.set_title("Sharon's Daily Revenue in June 2025")
    ax.set_ylabel("Revenue (Amount)")
    ax.set_xlabel("Date")
    ax.legend()
    plt.xticks(rotation=45)
    fig.tight_layout()
    return fig

def plot_july15(july15):
    # Sort by Revenue ascending
    july15_sorted = july15.sort_values("Revenue", ascending=True)
    fig, ax = plt.subplots()
    colors = []
    for _, row in july15_sorted.iterrows():
        if row["Revenue"] == july15_sorted["Revenue"].min():
            colors.append("red")
        elif row["Revenue"] == july15_sorted["Revenue"].max():
            colors.append("green")
        else:
            colors.append(salesman_colors[row["Salesman"]])
    bars = ax.bar(july15_sorted["Salesman"], july15_sorted["Revenue"], color=colors)
    for bar in bars:
        ax.annotate(f'{int(bar.get_height())}', 
                    (bar.get_x() + bar.get_width() / 2, bar.get_height()), 
                    ha='center', va='bottom', fontsize=9, color='black')
    ax.set_title("Revenue by Salesman on July 15, 2025")
    ax.set_ylabel("Revenue (Amount)")
    ax.set_xlabel("Salesman")
    fig.tight_layout()
    return fig

def plot_monthly_avg(monthly_avg):
    fig, ax = plt.subplots(figsize=(10,6))
    for salesman in monthly_avg.index:
        ax.plot(monthly_avg.columns, monthly_avg.loc[salesman], 
                marker="o", label=salesman, color=salesman_colors[salesman])
        for month in monthly_avg.columns:
            value = monthly_avg.loc[salesman, month]
            ax.annotate(f'{int(value)}', (month, value), textcoords="offset points", 
                       xytext=(0,5), ha='center', fontsize=8)
    ax.set_title("Average Monthly Revenue per Salesman")
    ax.set_ylabel("Average Revenue (Amount)")
    ax.set_xlabel("Month")
    ax.legend(title="Salesman")
    fig.tight_layout()
    return fig

def plot_oscar_extremes(oscar_low, oscar_high):
    fig, ax = plt.subplots()
    bars = ax.bar([oscar_low["Date"].strftime("%Y-%m-%d"), oscar_high["Date"].strftime("%Y-%m-%d")], 
                  [oscar_low["Revenue"], oscar_high["Revenue"]], 
                  color=["#8B5CF6", salesman_colors['Oscar']])
    for bar in bars:
        ax.annotate(f'{int(bar.get_height())}', 
                    (bar.get_x() + bar.get_width() / 2, bar.get_height()), 
                    ha='center', va='bottom', fontsize=9, color='black')
    ax.set_title("Oscar's Lowest & Highest Revenue Day")
    ax.set_ylabel("Revenue (Amount)")
    ax.set_xlabel("Date")
    fig.tight_layout()
    return fig

def plot_below_1000(below_1000):
    # Sort by count ascending
    below_1000_sorted = below_1000.sort_values(ascending=True)
    fig, ax = plt.subplots()
    colors = [salesman_colors[salesman] for salesman in below_1000_sorted.index]
    bars = ax.bar(below_1000_sorted.index, below_1000_sorted.values, color=colors)
    for p in ax.patches:
        ax.annotate(f'{int(p.get_height())}', 
                    (p.get_x() + p.get_width() / 2, p.get_height()), 
                    ha='center', va='bottom', fontsize=9, color='black')
    ax.set_title("Days with Revenue Below 1000 per Salesman")
    ax.set_ylabel("Number of Days")
    ax.set_xlabel("Salesman")
    fig.tight_layout()
    return fig

def plot_dec_revenue(dec_revenue):
    # Sort by revenue ascending
    dec_revenue_sorted = dec_revenue.sort_values(ascending=True)
    fig, ax = plt.subplots()
    colors = []
    for salesman in dec_revenue_sorted.index:
        if dec_revenue_sorted[salesman] == dec_revenue_sorted.max():
            colors.append("green")
        elif dec_revenue_sorted[salesman] == dec_revenue_sorted.min():
            colors.append("red")
        else:
            colors.append(salesman_colors[salesman])
    bars = ax.bar(dec_revenue_sorted.index, dec_revenue_sorted.values, color=colors)
    for bar in bars:
        ax.annotate(f'{int(bar.get_height())}', 
                    (bar.get_x() + bar.get_width() / 2, bar.get_height()), 
                    ha='center', va='bottom', fontsize=9, color='black')
    ax.set_title("Total Revenue per Salesman in December 2025")
    ax.set_ylabel("Revenue (Amount)")
    ax.set_xlabel("Salesman")
    fig.tight_layout()
    return fig

def plot_alex_extremes(alex_high, alex_low):
    fig, ax = plt.subplots()
    bars = ax.bar([alex_high["Date"].strftime("%Y-%m-%d"), alex_low["Date"].strftime("%Y-%m-%d")], 
                  [alex_high["Revenue"], alex_low["Revenue"]], 
                  color=[salesman_colors['Alexander'], "#BDC3C7"])
    for bar in bars:
        ax.annotate(f'{int(bar.get_height())}', 
                    (bar.get_x() + bar.get_width() / 2, bar.get_height()), 
                    ha='center', va='bottom', fontsize=9, color='black')
    ax.set_title("Alexander's Highest & Lowest Revenue Day")
    ax.set_ylabel("Revenue (Amount)")
    ax.set_xlabel("Date")
    fig.tight_layout()
    return fig

def plot_oscar_aug(oscar_aug):
    fig, ax = plt.subplots()
    ax.plot(oscar_aug["Date"], oscar_aug["Revenue"], marker="o", color=salesman_colors['Oscar'])
    for i, v in enumerate(oscar_aug["Revenue"]):
        ax.annotate(f'{int(v)}', (oscar_aug["Date"].iloc[i], v), ha='center', va='bottom', fontsize=9, color='black')
    ax.axhline(oscar_aug["Revenue"].mean(), color="green", linestyle="--", label="Mean")
    ax.axhline(oscar_aug["Revenue"].max(), color="orange", linestyle="--", label="Max")
    ax.axhline(oscar_aug["Revenue"].min(), color="red", linestyle="--", label="Min")
    ax.set_title("Oscar's Daily Revenue in August 2025")
    ax.set_ylabel("Revenue (Amount)")
    ax.set_xlabel("Date")
    ax.legend()
    plt.xticks(rotation=45)
    fig.tight_layout()
    return fig

def plot_nov_revenue(nov):
    # Sort by revenue ascending
    nov_sorted = nov.sort_values(ascending=True)
    fig, ax = plt.subplots()
    colors = []
    for salesman in nov_sorted.index:
        if nov_sorted[salesman] == nov_sorted.max():
            colors.append("green")
        elif nov_sorted[salesman] == nov_sorted.min():
            colors.append("red")
        else:
            colors.append(salesman_colors[salesman])
    bars = ax.bar(nov_sorted.index, nov_sorted.values, color=colors)
    for bar in bars:
        ax.annotate(f'{int(bar.get_height())}', 
                    (bar.get_x() + bar.get_width() / 2, bar.get_height()), 
                    ha='center', va='bottom', fontsize=9, color='black')
    ax.set_title("Total Revenue per Salesman in November 2025")
    ax.set_ylabel("Revenue (Amount)")
    ax.set_xlabel("Salesman")
    fig.tight_layout()
    return fig

# --- Data Preparation ---
perf = df.groupby("Salesman").agg(
    Total_Revenue=("Revenue", "sum"),
    Avg_Daily_Revenue=("Revenue", "mean"),
    Max_Revenue=("Revenue", "max"),
    Min_Revenue=("Revenue", "min")
).sort_values("Total_Revenue", ascending=False)

week_start = pd.Timestamp("2025-07-14")
week_end = pd.Timestamp("2025-07-20")
week_df = df[(df["Date"] >= week_start) & (df["Date"] <= week_end)]
weekly_revenue = week_df.groupby("Salesman")["Revenue"].sum()

sharon_june = df[(df["Salesman"]=="Sharon") & (df["Date"].dt.month==6)]
july15 = df[df["Date"]=="2025-07-15"].sort_values("Revenue")
monthly_avg = df.groupby([df["Salesman"], df["Date"].dt.month])["Revenue"].mean().unstack()
oscar = df[df["Salesman"]=="Oscar"]
oscar_low = oscar.loc[oscar["Revenue"].idxmin()]
oscar_high = oscar.loc[oscar["Revenue"].idxmax()]
below_1000 = df[df["Revenue"]<1000].groupby("Salesman").size()
dec_revenue = df[df["Date"].dt.month==12].groupby("Salesman")["Revenue"].sum()
alex = df[df["Salesman"]=="Alexander"]
alex_high = alex.loc[alex["Revenue"].idxmax()]
alex_low = alex.loc[alex["Revenue"].idxmin()]
oscar_aug = df[(df["Salesman"]=="Oscar") & (df["Date"].dt.month==8)]
nov = df[df["Date"].dt.month==11].groupby("Salesman")["Revenue"].sum()

# --- Tkinter UI with Tabs ---
root = tk.Tk()
root.title("Salesmen Revenue Dashboard")
notebook = ttk.Notebook(root)
notebook.pack(fill='both', expand=True)

def add_tab(fig, title):
    frame = ttk.Frame(notebook)
    notebook.add(frame, text=title)
    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill='both', expand=True)

# Add tabs for each visualization
add_tab(plot_general_overview(perf), "General Overview")
add_tab(plot_performance_table(perf), "Performance Table")
add_tab(plot_weekly_revenue(weekly_revenue), "Weekly Revenue")
add_tab(plot_sharon_june(sharon_june), "Sharon June")
add_tab(plot_july15(july15), "July 15 Revenue")
add_tab(plot_monthly_avg(monthly_avg), "Monthly Avg")
add_tab(plot_oscar_extremes(oscar_low, oscar_high), "Oscar Extremes")
add_tab(plot_below_1000(below_1000), "Below 1000 Days")
add_tab(plot_dec_revenue(dec_revenue), "December Revenue")
add_tab(plot_alex_extremes(alex_high, alex_low), "Alexander Extremes")
add_tab(plot_oscar_aug(oscar_aug), "Oscar August")
add_tab(plot_nov_revenue(nov), "November Revenue")

root.mainloop()