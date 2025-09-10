from db import init_db, add_expense, get_all_expenses, get_category_totals, get_total_spent
import matplotlib.pyplot as plt

init_db()  

while True:
    print("\n1. Add expense")
    print("2. Show expenses & reports")
    print("3. Show pie chart")
    print("4. Exit")
    choice = input("Choose option: ")

    if choice == "1":
        category = input("Enter category: ")
        amount = float(input("Enter amount: "))
        description = input("Enter description: ")
        add_expense(category, amount, description)
        print("Expense added!")

    elif choice == "2":
        expenses = get_all_expenses()
        for e in expenses:
            print(f"{e[1]} | {e[2]} | ₹{e[3]} | {e[4]}")
        print(f"\nTotal Spent: ₹{get_total_spent()}")
        print("\nCategory Totals:")
        for cat, total in get_category_totals():
            print(f"{cat}: ₹{total}")

    elif choice == "3":
        data = get_category_totals()
        if not data:
            print("No data for chart.")
        else:
            categories = [x[0] for x in data]
            amounts = [x[1] for x in data]
            plt.pie(amounts, labels=categories, autopct="%1.1f%%")
            plt.title("Expenses by Category 💸")
            plt.show()

    elif choice == "4":
        break

    else:
        print("Invalid choice!")
