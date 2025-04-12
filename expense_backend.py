import pymongo
from bson.objectid import ObjectId  # Import ObjectId

# Connect to MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["expense_db"]
collection = db["expenses"]

# 1. Add an Expense
def add_expense(category, amount, date, description):
    expense = {
        "category": category,
        "amount": amount,
        "date": date,
        "description": description
    }
    result = collection.insert_one(expense)  # Store the result
    print("Expense added successfully!  Inserted ID:", result.inserted_id) # Print the ID of the inserted document

# 2. Display All Expenses
def view_expenses():
    expenses = collection.find()
    for exp in expenses:
        print(exp)

# 3. Update an Expense (Based on ID)
def update_expense(expense_id, new_data):
    try:
        object_id = ObjectId(expense_id) #convert expense_id to ObjectId
        result = collection.update_one({"_id": object_id}, {"$set": new_data})
        if result.modified_count > 0:
            print("Expense updated successfully!")
        else:
            print("Expense not found or no changes made.")
    except Exception as e:
        print(f"Error updating expense: {e}")

# 4. Delete an Expense (Based on ID)
def delete_expense(expense_id):
    try:
        object_id = ObjectId(expense_id) #convert expense_id to ObjectId
        result = collection.delete_one({"_id": object_id})
        if result.deleted_count > 0:
            print("Expense deleted successfully!")
        else:
            print("Expense not found.")
    except Exception as e:
        print(f"Error deleting expense: {e}")

# Test Run (Executes only if this file is run directly)
if __name__ == "__main__":
    add_expense("Transport", 300, "2025-02-14", "Metro Ticket") #addded data
    print("All Expenses:")
    view_expenses()

    # Get the ID of the first expense for update and delete
    first_expense = collection.find_one()
    if first_expense:
        expense_id_to_update = first_expense["_id"]
        print(f"\nFirst Expense ID: {expense_id_to_update}") #printing the ID
        
        # Update the expense
        update_expense(str(expense_id_to_update), {"amount": 350, "description": "Metro Ticket Updated"})
        
        print("\nAll Expenses After Update:")
        view_expenses()
        
        # Delete the expense
        delete_expense(str(expense_id_to_update))
        
        print("\nAll Expenses After Delete:")
        view_expenses()
    else:
        print("\nNo expenses found to update or delete.")
