import os
from dotenv import load_dotenv
from data.datamanager import Data_Manager

load_dotenv()
Super-Username = os.getenv("CONTROLLER_USERNAME")
Super-Password = os.getenv("CONTROLLER_PASSWORD")

class User_Controller:
    
    def __init__(self, database: Data_Manager):
        self.db = database
    
    def add_user(self, username, password_hash, role, email):
        query = """
            INSERT INTO users (username, password_hash, role, email)
            VALUES (?, ?, ?, ?)
        """
        self.db.execute(query, (username, password_hash, role, email))

    def modify_user(self, userid, username, password_hash, role, email):
        query = """
            UPDATE users 
            SET username=?, password_hash=?, role=?, email=?
            WHERE userid=?
        """
        self.db.execute(query, (username, password_hash, role, email, userid))

    def delete_user(self, userid):
        self.db.execute("DELETE FROM users WHERE userid = ?", (userid,))

    def get_all_users(self):
        return self.db.fetch_all("SELECT * FROM users")

    def search_users(self, keyword):
        return self.db.fetch_all(
            "SELECT * FROM users WHERE username LIKE ?",
            (f"%{keyword}%",)
        )
    
