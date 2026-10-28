import csv
import os
from datetime import datetime

FILE_NAME = "expenses.csv"


def create_file():
    if not os.path.exists(FILE_NAME):
        with open(FILE_NAME, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Date", "Category", "Description", "Amount"])


def add_expense():
    date = input("Enter date (YYYY-MM-DD): ").strip()

    try:
        datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        print("Invalid date format.")
        return

    category = input("Enter category (Food, Travel, Shopping, etc.): ").strip()
    description = input("Enter description: ").strip()

    try:
        amount = float(input("Enter amount: "))
        if amount <= 0:
            print("Amount must be greater than zero.")
            return
    except ValueError:
        print("Please enter a valid amount.")
        return

    with open(FILE_NAME, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([date, category, description, amount])

    print("Expense added successfully.")


def read_expenses():
    expenses = []

    with open(FILE_NAME, "r", newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            expenses.append({
                "date": row["Date"],
                "category": row["Category"],
                "description": row["Description"],
                "amount": float(row["Amount"])
            })

    return expenses


def view_expenses():
    expenses = read_expenses()

    if len(expenses) == 0:
        print("No expenses recorded yet.")
        return

    print("\n--- All Expenses ---")
    for expense in expenses:
        print(
            expense["date"], "|",
            expense["category"], "|",
            expense["description"], "| Rs.",
            format(expense["amount"], ".2f")
        )


def show_monthly_total():
    month = input("Enter month (YYYY-MM): ").strip()

    try:
        datetime.strptime(month, "%Y-%m")
    except ValueError:
        print("Invalid month format.")
        return

    expenses = read_expenses()
    total = 0

    for expense in expenses:
        if expense["date"].startswith(month):
            total += expense["amount"]

    print("Total expenses for", month, ": Rs.", format(total, ".2f"))


def show_category_totals():
    expenses = read_expenses()
    totals = {}

    for expense in expenses:
        category = expense["category"]

        if category in totals:
            totals[category] += expense["amount"]
        else:
            totals[category] = expense["amount"]

    if len(totals) == 0:
        print("No expenses recorded yet.")
        return

    print("\n--- Spending by Category ---")
    for category, amount in sorted(totals.items(), key=lambda item: item[1], reverse=True):
        print(category, ": Rs.", format(amount, ".2f"))


def show_highest_expense():
    expenses = read_expenses()

    if len(expenses) == 0:
        print("No expenses recorded yet.")
        return

    highest = max(expenses, key=lambda expense: expense["amount"])

    print("\n--- Highest Expense ---")
    print("Date:", highest["date"])
    print("Category:", highest["category"])
    print("Description:", highest["description"])
    print("Amount: Rs.", format(highest["amount"], ".2f"))


def main():
    create_file()

    while True:
        print("\n===== Personal Expense Analyzer =====")
        print("1. Add Expense")
        print("2. View All Expenses")
        print("3. Show Monthly Total")
        print("4. Show Spending by Category")
        print("5. Show Highest Expense")
        print("6. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            add_expense()
        elif choice == "2":
            view_expenses()
        elif choice == "3":
            show_monthly_total()
        elif choice == "4":
            show_category_totals()
        elif choice == "5":
            show_highest_expense()
        elif choice == "6":
            print("Thank you for using Personal Expense Analyzer.")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
