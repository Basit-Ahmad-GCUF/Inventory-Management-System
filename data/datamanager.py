import sqlite3
from pathlib import Path

class Data_Manager:
    
    def __init__(self):
        db_name = "Inventory.db"
        # Store database file in the same folder as datamanager.py
        self.db_path = Path(__file__).parent / db_name
        
        # Connect to SQLite database
        self.connection = sqlite3.connect(str(self.db_path))
        
        # Allows accessing columns by name like dictionary keys (e.g., row["name"])
        self.connection.row_factory = sqlite3.Row
        
        # Creating a Pointer
        self.cursor = self.connection.cursor()
        
        # Automatically set up database structure on startup
        self.initialize_db()
    
    def initialize_db(self):
        # Creating the Tables If thy Don't Exist.
        
        self.cursor.execute("""
                            CREATE TABLE IF NOT EXISTS items (
                                id TEXT PRIMARY KEY,
                                name TEXT NOT NULL,
                                cost REAL NOT NULL,
                                quantity INTEGER NOT NULL,
                                description TEXT,
                                entry_date TEXT,
                                expirey_date TEXT
                            )
                            """)
        
        self.cursor.execute("""
                            CREATE TABLE IF NOT EXISTS users (
                                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                username TEXT UNIQUE NOT NULL,
                                password_hash TEXT NOT NULL,
                                role TEXT NOT NULL DEFAULT 'user',
                                email TEXT
                            )
                            """)
        
        self.cursor.execute("""
                            CREATE TABLE IF NOT EXISTS bill (
                                bill_id TEXT PRIMARY KEY,
                                biller TEXT NOT NULL,
                                datetime TEXT NOT NULL,
                                total_cost REAL NOT NULL
                            )
                            """)
        
        self.cursor.execute("""
                            CREATE TABLE IF NOT EXISTS bill_items (
                                bill_id TEXT NOT NULL,
                                item_id TEXT NOT NULL,
                                name TEXT NOT NULL,
                                cost REAL NOT NULL,
                                quantity INTEGER NOT NULL,
                                subtotal REAL NOT NULL
                            )
                            """)
        
        self.cursor.execute("""
                            CREATE TABLE IF NOT EXISTS settings (
                                name TEXT PRIMARY KEY,
                                value TEXT NOT NULL
                            )
                            """)
        
    def execute(self, query: str, params: tuple = ()):
        # Generic write method for INSERT, UPDATE, DELETE queries.
        self.cursor.execute(query, params)
        self.connection.commit()
        return self.cursor.lastrowid

    def fetch_all(self, query: str, params: tuple = ()):
        # Generic read method returning all matching rows.
        self.cursor.execute(query, params)
        return self.cursor.fetchall()

    def fetch_one(self, query: str, params: tuple = ()):
        # Generic read method returning a single matching row.
        self.cursor.execute(query, params)
        return self.cursor.fetchone()

    # ==================== ITEM OPERATIONS ====================
    def add_item(self, item_id, name, cost, quantity, description, entry_date, expiry_date):
        query = """
            INSERT INTO items (id, name, cost, quantity, description, entry_date, expiry_date)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        self.execute(query, (item_id, name, cost, quantity, description, entry_date, expiry_date))

    def modify_item(self, item_id, name, cost, quantity, description, entry_date, expiry_date):
        query = """
            UPDATE items 
            SET name=?, cost=?, quantity=?, description=?, entry_date=?, expiry_date=?
            WHERE id=?
        """
        self.execute(query, (name, cost, quantity, description, entry_date, expiry_date, item_id))

    def delete_item(self, item_id):
        self.execute("DELETE FROM items WHERE id = ?", (item_id,))

    def get_all_items(self):
        return self.fetch_all("SELECT * FROM items")
        
    def search_items(self, keyword):
        return self.fetch_all(
            "SELECT * FROM items WHERE name LIKE ?",
            (f"%{keyword}%",)
        )


    # ==================== USER OPERATIONS ====================
    def add_user(self, username, password_hash, role, email):
        query = """
            INSERT INTO users (username, password_hash, role, email)
            VALUES (?, ?, ?, ?)
        """
        self.execute(query, (username, password_hash, role, email))

    def modify_user(self, userid, username, password_hash, role, email):
        query = """
            UPDATE users 
            SET username=?, password_hash=?, role=?, email=?
            WHERE userid=?
        """
        self.execute(query, (username, password_hash, role, email, userid))

    def delete_user(self, userid):
        self.execute("DELETE FROM users WHERE userid = ?", (userid,))

    def get_all_users(self):
        return self.fetch_all("SELECT * FROM users")

    def search_users(self, keyword):
            return self.fetch_all(
                "SELECT * FROM users WHERE username LIKE ?",
                (f"%{keyword}%",)
            )


    # ==================== BILL OPERATIONS ====================
    def add_bill(self, bill_id, biller, datetime_str, total_cost, bill_items_list):
        """
        bill_items_list should be a list of tuples:
        [("Apple Watch", 1500.0, 2, 3000.0), ("Sound Bar", 1250.0, 1, 1250.0)]
        """
        # 1. Insert main bill info
        bill_query = "INSERT INTO bills (bill_id, biller, datetime, total_cost) VALUES (?, ?, ?, ?)"
        self.execute(bill_query, (bill_id, biller, datetime_str, total_cost))

        # 2. Insert all items associated with this bill
        item_query = "INSERT INTO bill_items (bill_id, item_id, name, cost, quantity, subtotal) VALUES (?, ?, ?, ?, ?)"
        for item_id, name, cost, qty, subtotal in bill_items_list:
            self.execute(item_query, (bill_id,item_id, name, cost, qty, subtotal))

    def get_all_bills(self):
        return self.fetch_all("SELECT * FROM bills")

    def get_bill_items(self, bill_id):
        return self.fetch_all("SELECT * FROM bill_items WHERE bill_id = ?", (bill_id,))

    def get_bill_by_id(self, bill_id):
        self.fetch_one(
            "SELECT * FROM bill WHERE bill_id = ?", (bill_id,)
        )