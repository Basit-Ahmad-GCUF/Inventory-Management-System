from datetime import date

class Inventory:
    
    def __init__(self, database):
        self.db = database
        pass
        
    def add_item(self, item_id, name, cost, quantity, description, entry_date, expiry_date):
        query = """
            INSERT INTO items (id, name, cost, quantity, description, entry_date, expiry_date)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        self.db.execute(query, (item_id, name, cost, quantity, description, entry_date, expiry_date))

    def modify_item(self, item_id, name, cost, quantity, description, entry_date, expiry_date):
        query = """
            UPDATE items 
            SET name=?, cost=?, quantity=?, description=?, entry_date=?, expiry_date=?
            WHERE id=?
        """
        self.db.execute(query, (name, cost, quantity, description, entry_date, expiry_date, item_id))

    def delete_item(self, item_id):
        self.db.execute("DELETE FROM items WHERE id = ?", (item_id,))

    def get_all_items(self):
        return self.db.fetch_all("SELECT * FROM items")
    
    def get_item_by_id(self, id):
        return self.db.fetch_one(
            "SELECT * FROM items WHERE id = ?",
            (id,)
            )
    
    def get_item_by_name(self, name):
        return self.db.fetch_one(
            "SELECT * FROM items WHERE name = ?",
            (name,)
            )
    
    def search_items(self, keyword):
        return self.db.fetch_all(
            "SELECT * FROM items WHERE name LIKE ?",
            (f"%{keyword}%",)
        )
    
    def deduct_stock(self, item_id, quantity_sold):
        self.db.execute(
            "UPDATE items SET quantity = quantity - ? WHERE id = ?",
            (quantity_sold, item_id)
        )