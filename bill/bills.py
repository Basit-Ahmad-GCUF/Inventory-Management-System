from bill_item import BillItem
from data.datamanager import Data_Manager
from datetime import datetime

class Bill:
    inventoryfilename = "inventory_data.json"
    filenameitems = "bill_data.json"
    filenameInfo = "bill_info.json"
    
    def __init__(self):
        self.data_manager = Data_Manager()
        self.cart = []
    
    def add_item_to_cart(self):
        print("Add item to cart")
        Product_ID = input("Enter Product ID: ")
        item = self.data_manager.find_data(self.inventoryfilename, Product_ID, 'id')
        if item:
            while True:
                try:
                    quantity = int(input(f"Enter quantity for {item['name']} (Available: {item['quantity']}): "))
                    if quantity <= 0:
                        print("Quantity must be greater than zero. Please try again.")
                        continue
                    if quantity > item['quantity']:
                        print(f"Insufficient stock. Only {item['quantity']} available. Please try again.")
                        continue
                    self.cart.append(BillItem(item['id'], item['name'], item['cost'], quantity))
                    break
                except ValueError:
                    print("Invalid input. Please enter a valid integer for quantity.")
        else:
            print(f"No item found with Product ID '{Product_ID}'.")

    def remove_item_from_cart(self):
        print("Remove item from cart")
        Product_Name = input("Enter Product name to remove: ")
        for i, item in enumerate(self.cart):
            if item.name == Product_Name:
                del self.cart[i]
                print(f"Item with Product name '{Product_Name}' removed from cart.")
                return
        print(f"No item found in cart with Product name '{Product_Name}'.")
    
    def finalize_bill(self,logged_in_user):
        
        items_info = []
        deducted_items = []
        
        if not self.cart:
            print("Cart is empty. Cannot finalize bill.")
            return
        
        for c in self.cart:
            print(f"Product ID: {c.id}, Name: {c.name}, Cost: {c.cost}, Quantity: {c.quantity}")
        total_cost = sum(item.cost * item.quantity for item in self.cart)
        print(f"Total \t:\t {total_cost}")
        
        bill_info = {
            "Bill_id": f"bill_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "Date/Time": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
            "Biller": logged_in_user,
            "Total_Items": len(self.cart),
            "Total": total_cost
            }
        
        for c in self.cart:
            items_info.append({
            "Bill_id": bill_info["Bill_id"],
            "Product_ID": c.id,
            "Name": c.name,
            "Cost": c.cost,
            "Quantity": c.quantity
            })
            deducted_items.append({
                "id": c.id  ,
                "quantity": c.quantity
            })    

        self.data_manager.add_data(self.filenameInfo, bill_info)
        self.data_manager.add_data(self.filenameitems, items_info)

        return deducted_items