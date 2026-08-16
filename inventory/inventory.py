from item import Item
import datamanager
from datetime import date

class Inventory:
    
    filename = "inventory_data.json"
    
    def __init__(self):
        self.data_manager = datamanager.Data_Manager()
    
    def load_inventory(self):
        return self.data_manager.load_data(self.filename)
        
    def add_item(self):
        item_id = input("Enter item ID: ")
        name = input("Enter item name: ")
        quantity = int(input("Enter item quantity: "))
        cost = float(input("Enter item cost: "))
        description = input("Enter item description: ")
        entry_date = date.today().strftime("%d-%m-%Y")
        expiry_date = input("Enter item expiry date (DD-MM-YYYY): ")
        
        new_item = Item(item_id, name, quantity, cost, description, entry_date, expiry_date)
        self.data_manager.add_data(self.filename, new_item.to_dict())
        print(f"Item '{name}' added successfully.")
    
    def show_item(self,item):
        print(dict(item))
    
    def delete_item(self):
        item_name = input("Enter the Name of the item to delete: ")
        item_to_delete = self.data_manager.find_data(self.filename, item_name, 'name')
        if item_to_delete:
            self.show_item(item_to_delete)
            confirm = input(f"Are you sure you want to delete item with Name '{item_name}'? (yes/no): ")
            if confirm.lower() == 'yes':
                self.data_manager.delete_data(self.filename, item_to_delete['id'])
                print(f"Item with Name '{item_name}' deleted successfully.")
            else:
                print("Deletion cancelled.")
        else:
            print(f"No item found with Name '{item_name}'.")
    
    def update_item(self):
        item_name = input("Enter the Name of the item to update: ")
        existing_item = self.data_manager.find_data(self.filename, item_name, 'name')
        
        if existing_item:
            self.show_item(existing_item)
            name = input(f"Enter new name (current: {existing_item['name']}): ") or existing_item['name']
            quantity = input(f"Enter new quantity (current: {existing_item['quantity']}): ") or existing_item['quantity']
            cost = input(f"Enter new cost (current: {existing_item['cost']}): ") or existing_item['cost']
            description = input(f"Enter new description (current: {existing_item['description']}): ") or existing_item['description']
            entry_date = date.today()
            expiry_date = input(f"Enter new expiry date (current: {existing_item['expiry_date']}): ") or existing_item['expiry_date']
            
            updated_item = Item(existing_item['id'], name, int(quantity), float(cost), description, entry_date, expiry_date)
            self.data_manager.update_data(self.filename, existing_item['id'], updated_item.to_dict())
            print(f"Item with Name '{item_name}' updated successfully.")
        else:
            print(f"No item found with Name '{item_name}'.")
    
    def view_inventory(self):
        inventory_data = self.load_inventory()
        if inventory_data:
            print("Current Inventory:")
            for item in inventory_data:
                self.show_item(item)
        else:
            print("Inventory is empty.")
    
    def search_items(self):
        item_name = input("Enter the Name of the item to search: ")
        found_items = self.data_manager.find_data(self.filename, item_name, 'name')
        if found_items:
            print("Items found:")
            for item in found_items:
                self.show_item(item)
        else:
            print(f"No items found with Name '{item_name}'.")
    
    def deduct_item_quantity(self,item_name,amount_to_deduct):
        existing_item = self.data_manager.find_data(self.filename, item_name, 'name')
        
        if existing_item:
            self.show_item(existing_item)
            if amount_to_deduct <= existing_item['quantity']:
                existing_item['quantity'] -= amount_to_deduct
                self.data_manager.update_data(self.filename, existing_item['id'], existing_item)
                
                