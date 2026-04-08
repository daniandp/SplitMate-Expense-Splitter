import sqlite3

# Database file responsibility: Handle SQLite3 operations

class ExpenseDB:
    def __init__(self):
        self.db_name = "expenses.db"
        self.create_tables()

    def create_tables(self):
        conn = None
        try:
            # Establish connection with the database
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            
            # Create members table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS members (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL UNIQUE
                )
            ''')
            
            # Create expenses table with a foreign key linked to members
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS expenses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    description TEXT NOT NULL,
                    amount REAL NOT NULL,
                    payer_id INTEGER NOT NULL,
                    FOREIGN KEY(payer_id) REFERENCES members(id)
                )
            ''')
            conn.commit() # Save changes
            
        except sqlite3.Error as err:
            # Catch database specific errors and print them for debugging
            print("Database Error:", err)
        finally:
            # Close the connection
            if conn != None:
                conn.close()

    # -------------------------- CRUD ---------------------------
    # --- CREATE ---
    def add_member(self, name):
        conn = None
        success = False
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO members (name) VALUES (?)", (name,))
            conn.commit()
            success = True
        except sqlite3.Error as err:
            print("Error adding member:", err)
            success = False
        finally:
            if conn != None:
                conn.close()
        return success

    def add_expense(self, description, amount, payer_id):
        conn = None
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO expenses (description, amount, payer_id) VALUES (?, ?, ?)",
                           (description, amount, payer_id))
            conn.commit()
        except sqlite3.Error as err:
            print("Error adding expense:", err)
        finally:
            if conn != None:
                conn.close()

    # --- READ ---
    def get_members(self):
        conn = None
        results = []
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            print('\nMembers in the database:')
            cursor.execute("SELECT * FROM members")
            # Fetch all records from the query
            results = cursor.fetchall()
            for row in results:
                print(row)
        except sqlite3.Error as err:
            print("Error reading members:", err)
        finally:
            if conn != None:
                conn.close()
        return results

    def get_expenses(self):
        conn = None
        results = []
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            print('\nExpenses in the database:')
            cursor.execute('''
                SELECT expenses.id, expenses.description, expenses.amount, members.name
                FROM expenses
                JOIN members ON expenses.payer_id = members.id
            ''')
            results = cursor.fetchall()
            for row in results:
                print(row)  
        except sqlite3.Error as err:
            print("Error reading expenses:", err)
        finally:
            if conn != None:
                conn.close()
        return results

    # --- UPDATE ---
    def update_expense(self, expense_id, new_desc, new_amount):
        conn = None
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            # Update specific records based on the expense_id
            cursor.execute("UPDATE expenses SET description=?, amount=? WHERE id=?",
                           (new_desc, new_amount, expense_id))
            conn.commit()
        except sqlite3.Error as err:
            print("Error updating expense:", err)
        finally:
            if conn != None:
                conn.close()

    # --- DELETE ---
    def delete_member(self, member_id):
        conn = None
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            # Deleting the member
            cursor.execute("DELETE FROM members WHERE id=?", (member_id,))
            # Deleting associated expenses
            cursor.execute("DELETE FROM expenses WHERE payer_id=?", (member_id,))
            conn.commit()
        except sqlite3.Error as err:
            print("Error deleting member:", err)
        finally:
            if conn != None:
                conn.close()

    def delete_expense(self, expense_id):
        conn = None
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute("DELETE FROM expenses WHERE id=?", (expense_id,))
            conn.commit()
        except sqlite3.Error as err:
            print("Error deleting expense:", err)
        finally:
            if conn != None:
                conn.close()