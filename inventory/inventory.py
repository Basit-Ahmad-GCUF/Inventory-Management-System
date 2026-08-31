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
    
    def get_item_by_id(self, item_id):
        return self.db.get_item_by_id(item_id)
    
    def get_item_by_name(self, item_name):
        return self.db.get_item_by_name(item_name)
    
    def search_items(self, keyword):
        return self.db.search_items(keyword)
    
    def deduct_stock(self, item_id, quantity_sold):
        self.db.deduct_stock_from_inventory(item_id, quantity_sold)