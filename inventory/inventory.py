from datetime import date

class Inventory:
    
    def __init__(self, database):
        self.db = database
        pass
    
    def add_item(self, id, name, cost, quantity, desctiption, entry_date, expirey_date):
        self.db.add_item(id, name, cost, quantity, desctiption, entry_date, expirey_date)
        
    def delete_item(self, id_to_remove):
        self.db.delete_item(id_to_remove)
    
    def modify_item(self, item_id_to_modify, name, cost, quantity, description, entry_date, expiry_date):
        self.db.modify_item(item_id_to_modify, name, cost, quantity, description, entry_date, expiry_date)
    
    def get_all_items(self):
        return self.db.get_all_items()
    
    def search_items(self, keyword):
        return self.db.search_items(keyword)
    