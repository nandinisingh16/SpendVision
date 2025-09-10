import pandas as pd
import os
from datetime import datetime
import matplotlib.pyplot as plt

FILE_NAME = "expenses.csv"

# --- Save Expense ---
def save_transaction(amount, category):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    df = pd.DataFrame([[timestamp, float(amount), category]],
                      columns=["Date", "Amount", "Category"])
    
    if os.path.exists(FILE_NAME):
        df.to_csv(FILE_NAME, mode='a', header=False, index=False)
    else:
        df.to_csv(FILE_NAME, index=False)
    
    print(f" Saved: ₹{amount} in {category} at {timestamp}")

# --- Show All Expenses & Reports ---
def show_expenses():
    if not os.path.exists(FILE_NAME):
        print("⚠ No expenses recorded yet.")
        return None
    
    # Read CSV with headers
    df = pd.read_csv(FILE_NAME)

    # Ensure amount is numeric
    df["Amount"] = pd.to_numeric(df["Amount"], errors="coerce").fillna(0)

    print("\n--- Expense History ---")
    print(df.to_string(index=False))
    
    # Total spent
    total = df["Amount"].sum()
    print(f"\n Total Spent: ₹{total}")
    
    # Category-wise spending
    print("\n Category-wise Spending:")
    category_sum = df.groupby("Category")["Amount"].sum()
    print(category_sum)
    
    return df

# --- Show Pie Chart ---
def show_expense_chart():
    if not os.path.exists(FILE_NAME):
        print(" No expenses to show.")
        return
    
    df = pd.read_csv(FILE_NAME)

    # Ensure amount is numeric
    df["Amount"] = pd.to_numeric(df["Amount"], errors="coerce").fillna(0)
    
    if df.empty:
        print(" No expenses to show.")
        return

    category_sum = df.groupby("Category")["Amount"].sum()

    plt.figure(figsize=(6, 6))
    plt.pie(category_sum, labels=category_sum.index,
            autopct='%1.1f%%', startangle=140)
    plt.title(" Expenses by Category")
    plt.show()
