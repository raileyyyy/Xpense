import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

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
    fig, ax = plt.subplots()
    total_revenue = perf["Total_Revenue"]
    colors = [salesman_colors[salesman] for salesman in total_revenue.index]
    bars = ax.bar(total_revenue.index, total_revenue.values, color=colors)
    for bar in bars:
        ax.annotate(f'{int(bar.get_height()):,}', 
                    (bar.get_x() + bar.get_width() / 2, bar.get_height()), 
                    ha='center', va='bottom', fontsize=10, color='black')
    plt.title("Total Revenue per Salesman (2025)")
    plt.ylabel("Total Revenue")
    plt.xlabel("Salesman")
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, p: f'{int(x):,}'))
    plt.tight_layout()
    plt.show()

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
    plt.tight_layout()
    plt.show()

def plot_weekly_revenue(weekly_revenue):
    fig, ax = plt.subplots()
    colors = [salesman_colors[salesman] for salesman in weekly_revenue.index]
    bars = weekly_revenue.plot(kind="bar", color=colors, ax=ax)
    plt.title("Total Revenue per Salesman (Week of July 14–20, 2025)")
    plt.ylabel("Revenue (Amount)")
    plt.xlabel("Salesman")
    annotate_bars(ax)
    plt.tight_layout()
    plt.show()

def plot_sharon_june(sharon_june):
    fig, ax = plt.subplots()
    ax.plot(sharon_june["Date"], sharon_june["Revenue"], marker="o", label="Daily Revenue", color=salesman_colors['Sharon'])
    for i, v in enumerate(sharon_june["Revenue"]):
        ax.annotate(f'{int(v)}', (sharon_june["Date"].iloc[i], v), ha='center', va='bottom', fontsize=9, color='black')
    ax.axhline(sharon_june["Revenue"].max(), color="green", linestyle="--", label="Max")
    ax.axhline(sharon_june["Revenue"].min(), color="red", linestyle="--", label="Min")
    plt.title("Sharon's Daily Revenue in June 2025")
    plt.ylabel("Revenue (Amount)")
    plt.xlabel("Date")
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def plot_july15(july15):
    fig, ax = plt.subplots()
    colors = []
    for _, row in july15.iterrows():
        if row["Revenue"] == july15["Revenue"].min():
            colors.append("red")
        elif row["Revenue"] == july15["Revenue"].max():
            colors.append("green")
        else:
            colors.append(salesman_colors[row["Salesman"]])
    bars = ax.bar(july15["Salesman"], july15["Revenue"], color=colors)
    for bar in bars:
        ax.annotate(f'{int(bar.get_height())}', 
                    (bar.get_x() + bar.get_width() / 2, bar.get_height()), 
                    ha='center', va='bottom', fontsize=9, color='black')
    plt.title("Revenue by Salesman on July 15, 2025")
    plt.ylabel("Revenue (Amount)")
    plt.xlabel("Salesman")
    plt.tight_layout()
    plt.show()

def plot_monthly_avg(monthly_avg):
    fig, ax = plt.subplots(figsize=(10,6))
    for salesman in monthly_avg.index:
        ax.plot(monthly_avg.columns, monthly_avg.loc[salesman], 
                marker="o", label=salesman, color=salesman_colors[salesman])
        for month in monthly_avg.columns:
            value = monthly_avg.loc[salesman, month]
            ax.annotate(f'{int(value)}', (month, value), textcoords="offset points", 
                       xytext=(0,5), ha='center', fontsize=8)
    plt.title("Average Monthly Revenue per Salesman")
    plt.ylabel("Average Revenue (Amount)")
    plt.xlabel("Month")
    plt.legend(title="Salesman")
    plt.tight_layout()
    plt.show()

def plot_oscar_extremes(oscar_low, oscar_high):
    fig, ax = plt.subplots()
    bars = ax.bar([oscar_low["Date"].strftime("%Y-%m-%d"), oscar_high["Date"].strftime("%Y-%m-%d")], 
                  [oscar_low["Revenue"], oscar_high["Revenue"]], 
                  color=["#8B5CF6", salesman_colors['Oscar']])
    for bar in bars:
        ax.annotate(f'{int(bar.get_height())}', 
                    (bar.get_x() + bar.get_width() / 2, bar.get_height()), 
                    ha='center', va='bottom', fontsize=9, color='black')
    plt.title("Oscar's Lowest & Highest Revenue Day")
    plt.ylabel("Revenue (Amount)")
    plt.xlabel("Date")
    plt.tight_layout()
    plt.show()

def plot_below_1000(below_1000):
    fig, ax = plt.subplots()
    colors = [salesman_colors[salesman] for salesman in below_1000.index]
    bars = below_1000.plot(kind="bar", color=colors, ax=ax)
    for p in ax.patches:
        ax.annotate(f'{int(p.get_height())}', 
                    (p.get_x() + p.get_width() / 2, p.get_height()), 
                    ha='center', va='bottom', fontsize=9, color='black')
    plt.title("Days with Revenue Below 1000 per Salesman")
    plt.ylabel("Number of Days")
    plt.xlabel("Salesman")
    plt.tight_layout()
    plt.show()

def plot_dec_revenue(dec_revenue):
    fig, ax = plt.subplots()
    colors = []
    for salesman in dec_revenue.index:
        if dec_revenue[salesman] == dec_revenue.max():
            colors.append("green")
        elif dec_revenue[salesman] == dec_revenue.min():
            colors.append("red")
        else:
            colors.append(salesman_colors[salesman])
    bars = ax.bar(dec_revenue.index, dec_revenue.values, color=colors)
    for bar in bars:
        ax.annotate(f'{int(bar.get_height())}', 
                    (bar.get_x() + bar.get_width() / 2, bar.get_height()), 
                    ha='center', va='bottom', fontsize=9, color='black')
    plt.title("Total Revenue per Salesman in December 2025")
    plt.ylabel("Revenue (Amount)")
    plt.xlabel("Salesman")
    plt.tight_layout()
    plt.show()

def plot_alex_extremes(alex_high, alex_low):
    fig, ax = plt.subplots()
    bars = ax.bar([alex_high["Date"].strftime("%Y-%m-%d"), alex_low["Date"].strftime("%Y-%m-%d")], 
                  [alex_high["Revenue"], alex_low["Revenue"]], 
                  color=[salesman_colors['Alexander'], "#BDC3C7"])
    for bar in bars:
        ax.annotate(f'{int(bar.get_height())}', 
                    (bar.get_x() + bar.get_width() / 2, bar.get_height()), 
                    ha='center', va='bottom', fontsize=9, color='black')
    plt.title("Alexander's Highest & Lowest Revenue Day")
    plt.ylabel("Revenue (Amount)")
    plt.xlabel("Date")
    plt.tight_layout()
    plt.show()

def plot_oscar_aug(oscar_aug):
    fig, ax = plt.subplots()
    ax.plot(oscar_aug["Date"], oscar_aug["Revenue"], marker="o", color=salesman_colors['Oscar'])
    for i, v in enumerate(oscar_aug["Revenue"]):
        ax.annotate(f'{int(v)}', (oscar_aug["Date"].iloc[i], v), ha='center', va='bottom', fontsize=9, color='black')
    ax.axhline(oscar_aug["Revenue"].mean(), color="green", linestyle="--", label="Mean")
    ax.axhline(oscar_aug["Revenue"].max(), color="orange", linestyle="--", label="Max")
    ax.axhline(oscar_aug["Revenue"].min(), color="red", linestyle="--", label="Min")
    plt.title("Oscar's Daily Revenue in August 2025")
    plt.ylabel("Revenue (Amount)")
    plt.xlabel("Date")
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def plot_nov_revenue(nov):
    fig, ax = plt.subplots()
    colors = []
    for salesman in nov.index:
        if nov[salesman] == nov.max():
            colors.append("green")
        elif nov[salesman] == nov.min():
            colors.append("red")
        else:
            colors.append(salesman_colors[salesman])
    bars = ax.bar(nov.index, nov.values, color=colors)
    for bar in bars:
        ax.annotate(f'{int(bar.get_height())}', 
                    (bar.get_x() + bar.get_width() / 2, bar.get_height()), 
                    ha='center', va='bottom', fontsize=9, color='black')
    plt.title("Total Revenue per Salesman in November 2025")
    plt.ylabel("Revenue (Amount)")
    plt.xlabel("Salesman")
    plt.tight_layout()
    plt.show()


# Create the performance summary DataFrame
perf = df.groupby("Salesman").agg(
    Total_Revenue=("Revenue", "sum"),
    Avg_Daily_Revenue=("Revenue", "mean"),
    Max_Revenue=("Revenue", "max"),
    Min_Revenue=("Revenue", "min")
).sort_values("Total_Revenue", ascending=False)

# --- Call your visualization functions below ---

print("\nGeneral Overview:")
print(perf)
plot_general_overview(perf)
plot_performance_table(perf)

# Question 1
week_start = pd.Timestamp("2025-07-14")
week_end = pd.Timestamp("2025-07-20")
week_df = df[(df["Date"] >= week_start) & (df["Date"] <= week_end)]
weekly_revenue = week_df.groupby("Salesman")["Revenue"].sum()
print("\nQ1: Weekly revenue (July 14–20, 2025):")
print(f"\nHighest revenue: {weekly_revenue.idxmax()} - {weekly_revenue.max():,}")
print(f"Lowest revenue: {weekly_revenue.idxmin()} - {weekly_revenue.min():,}")
plot_weekly_revenue(weekly_revenue)

# Question 2
sharon_june = df[(df["Salesman"]=="Sharon") & (df["Date"].dt.month==6)]
print("\nQ2: Sharon's total revenue in June 2025:\n")
print(f"Total: {sharon_june['Revenue'].sum():,}")
print(f"\nHighest daily revenue: {sharon_june['Revenue'].max():,}")
print(f"Lowest daily revenue: {sharon_june['Revenue'].min():,}")
plot_sharon_june(sharon_june)

# Question 3
july15 = df[df["Date"]=="2025-07-15"].sort_values("Revenue")
print("\nQ3: Revenue by Salesman on July 15, 2025:")
print(july15[["Salesman", "Revenue"]])
print(f"\nHighest: {july15.iloc[-1]['Salesman']} - {july15.iloc[-1]['Revenue']:,}")
print(f"Lowest: {july15.iloc[0]['Salesman']} - {july15.iloc[0]['Revenue']:,}")
plot_july15(july15)

# Question 4
monthly_avg = df.groupby([df["Salesman"], df["Date"].dt.month])["Revenue"].mean().unstack()
print("\nQ4: Average monthly revenue per salesman:\n")
print(monthly_avg)
plot_monthly_avg(monthly_avg)

# Question 5
oscar = df[df["Salesman"]=="Oscar"]
oscar_low = oscar.loc[oscar["Revenue"].idxmin()]
oscar_high = oscar.loc[oscar["Revenue"].idxmax()]
print("\nQ5: Oscar's lowest and highest revenue:")
print(f"\nLowest: {oscar_low['Revenue']:,} on {oscar_low['Date'].date()}")
print(f"Highest: {oscar_high['Revenue']:,} on {oscar_high['Date'].date()}")
plot_oscar_extremes(oscar_low, oscar_high)

# Question 6
below_1000 = df[df["Revenue"]<1000].groupby("Salesman").size()
print("\nQ6: Days with revenue below 1000 per salesman:")
print(f"\nMost days <1000: {below_1000.idxmax()} - {below_1000.max()}")
print(f"Least days <1000: {below_1000.idxmin()} - {below_1000.min()}")
plot_below_1000(below_1000)

# Question 7
dec_revenue = df[df["Date"].dt.month==12].groupby("Salesman")["Revenue"].sum()
print("\nQ7: Total revenue per salesman in December 2025:")
print(f"\nHighest: {dec_revenue.idxmax()} - {dec_revenue.max():,}")
print(f"Lowest: {dec_revenue.idxmin()} - {dec_revenue.min():,}")
plot_dec_revenue(dec_revenue)

# Question 8
alex = df[df["Salesman"]=="Alexander"]
alex_high = alex.loc[alex["Revenue"].idxmax()]
alex_low = alex.loc[alex["Revenue"].idxmin()]
print("\nQ8: Alexander's highest and lowest revenue:")
print(f"\nHighest: {alex_high['Revenue']:,} on {alex_high['Date'].date()}")
print(f"Lowest: {alex_low['Revenue']:,} on {alex_low['Date'].date()}")
plot_alex_extremes(alex_high, alex_low)

# Question 9
oscar_aug = df[(df["Salesman"]=="Oscar") & (df["Date"].dt.month==8)]
print("\nQ9: Oscar's daily revenue in August 2025:")
print(f"\nAverage: {oscar_aug['Revenue'].mean():,.2f}")
print(f"\nMax: {oscar_aug['Revenue'].max():,}")
print(f"Min: {oscar_aug['Revenue'].min():,}")
plot_oscar_aug(oscar_aug)

# Question 10
nov = df[df["Date"].dt.month==11].groupby("Salesman")["Revenue"].sum()
print("\nQ10: Total revenue per salesman in November 2025:")
print(f"\nHighest: {nov.idxmax()} - {nov.max():,}")
print(f"Lowest: {nov.idxmin()} - {nov.min():,}")
plot_nov_revenue(nov)