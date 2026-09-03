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
                                expiry_date TEXT
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