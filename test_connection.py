import pymongo

# Connect to MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")

# Print the list of available databases
db_list = client.list_database_names()
print("Available Databases:", db_list)

# Select the Expense Tracker database
db = client["expense_db"]
collection = db["expenses"]

# Insert a test expense
expense = {"category": "Food", "amount": 100, "date": "2025-02-14", "description": "Test Entry"}
collection.insert_one(expense)

# Print all expenses
print("All Expenses:")
for expense in collection.find():
    print(expense)
