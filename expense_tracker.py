import tkinter as tk
from tkinter import ttk, messagebox
import pymongo
from datetime import datetime

# MongoDB Connection
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["expense_db"]
expense_collection = db["expenses"]
income_collection = db["income"]

# --- Database Interaction Functions ---

# 1. Add an Expense
def add_expense_to_db(category, amount, date, description):
    expense = {
        "category": category,
        "amount": amount,
        "date": date,
        "description": description
    }
    expense_collection.insert_one(expense)

# 2. Add Income
def add_income_to_db(source, amount, date):
    income = {
        "source": source,
        "amount": amount,
        "date": date
    }
    income_collection.insert_one(income)

# 3. Display All Expenses and Income
def get_all_expenses():
    return list(expense_collection.find())  # Return as a list

def get_all_income():
    return list(income_collection.find())

# 4. Remove an Expense or Income (Based on values)
def remove_entry_from_db(entry_type, category_source, amount, date, description=""):
    if entry_type == "Expense":
        expense_collection.delete_one({
            "category": category_source,
            "amount": amount,
            "date": date,
            "description": description
        })
    elif entry_type == "Income":
        income_collection.delete_one({
            "source": category_source,
            "amount": amount,
            "date": date
        })

# --- GUI Functions ---

def add_expense():
    category = category_var.get()
    amount = amount_var.get()
    description = description_var.get()
    date = datetime.now().strftime("%d-%m-%y")

    if not category or not amount.isdigit():
        messagebox.showerror("Error", "Please enter valid details!")
        return

    add_expense_to_db(category, int(amount), date, description)
    update_display()
    clear_expense_inputs()

def add_income():
    source = income_source_var.get()
    amount = income_amount_var.get()
    date = datetime.now().strftime("%d-%m-%y")

    if not source or not amount.isdigit():
        messagebox.showerror("Error", "Please enter valid details!")
        return

    add_income_to_db(source, int(amount), date)
    update_display()
    clear_income_inputs()

def remove_selected():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showinfo("Info", "Please select an item to remove.")
        return

    selected_item = selected_item[0]
    values = tree.item(selected_item, "values")
    if not values:
        messagebox.showinfo("Info", "Please select a valid item to remove.")
        return
    entry_type = values[0]
    category_source = values[1]
    amount = int(values[2])
    date = values[3]
    description = values[4]  # Get the description

    remove_entry_from_db(entry_type, category_source, amount, date, description)
    update_display()

def update_display():
    tree.delete(*tree.get_children())
    total_income = 0
    total_expense = 0

    incomes = get_all_income()
    for income in incomes:
        tree.insert("", "end", values=("Income", income["source"], income["amount"], income["date"], ""))
        total_income += income["amount"]

    expenses = get_all_expenses()
    for expense in expenses:
        tree.insert("", "end", values=("Expense", expense["category"], expense["amount"], expense["date"], expense["description"]))
        total_expense += expense["amount"]

    balance_var.set(f"Total Balance: {total_income - total_expense}")

def clear_expense_inputs():
    category_var.set("")
    amount_var.set("")
    description_var.set("")

def clear_income_inputs():
    income_source_var.set("")
    income_amount_var.set("")

# --- GUI Setup ---

root = tk.Tk()
root.title("Expense Tracker")
root.configure(bg="black")
root.geometry("700x500")

# Fonts and Colors
font_style = ("Arial", 12, "bold")
fg_color = "white"
bg_color = "black"

# Expense Inputs
tk.Label(root, text="Category:", font=font_style, fg=fg_color, bg=bg_color).grid(row=0, column=0, padx=10, pady=5, sticky="w")
category_var = tk.StringVar()
category_entry = tk.Entry(root, textvariable=category_var, font=font_style)
category_entry.grid(row=0, column=1, padx=10, pady=5)

tk.Label(root, text="Amount:", font=font_style, fg=fg_color, bg=bg_color).grid(row=1, column=0, padx=10, pady=5, sticky="w")
amount_var = tk.StringVar()
amount_entry = tk.Entry(root, textvariable=amount_var, font=font_style)
amount_entry.grid(row=1, column=1, padx=10, pady=5)

tk.Label(root, text="Description:", font=font_style, fg=fg_color, bg=bg_color).grid(row=2, column=0, padx=10, pady=5, sticky="w")
description_var = tk.StringVar()
description_entry = tk.Entry(root, textvariable=description_var, font=font_style)
description_entry.grid(row=2, column=1, padx=10, pady=5)

tk.Button(root, text="Add Expense", command=add_expense, font=font_style, bg="green", fg="white").grid(row=3, column=1, padx=10, pady=5)

# Income Inputs
tk.Label(root, text="Income Source:", font=font_style, fg=fg_color, bg=bg_color).grid(row=0, column=2, padx=10, pady=5, sticky="w")
income_source_var = tk.StringVar()
income_source_entry = tk.Entry(root, textvariable=income_source_var, font=font_style)
income_source_entry.grid(row=0, column=3, padx=10, pady=5)

tk.Label(root, text="Income Amount:", font=font_style, fg=fg_color, bg=bg_color).grid(row=1, column=2, padx=10, pady=5, sticky="w")
income_amount_var = tk.StringVar()
income_amount_entry = tk.Entry(root, textvariable=income_amount_var, font=font_style)
income_amount_entry.grid(row=1, column=3, padx=10, pady=5)

tk.Button(root, text="Add Income", command=add_income, font=font_style, bg="blue", fg="white").grid(row=3, column=3, padx=10, pady=5)

# Table
columns = ("Type", "Category/Source", "Amount", "Date", "Description")
tree = ttk.Treeview(root, columns=columns, show="headings", height=10)
tree.grid(row=4, column=0, columnspan=4, padx=10, pady=10)

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=120, anchor="center")

# Remove Button
tk.Button(root, text="Remove Selected", command=remove_selected, font=font_style, bg="red", fg="white").grid(row=5, column=1, columnspan=2, pady=10)

# Total Balance
balance_var = tk.StringVar()
balance_label = tk.Label(root, textvariable=balance_var, font=font_style, fg="green", bg=bg_color)
balance_label.grid(row=6, column=0, columnspan=4, pady=10)

# Initialize Data
update_display()

root.mainloop()
