from bills import Bill

class Billing_Manager:
    filenamebillinfo = "bill_info.json"
    filenamebillitems = "bill_data.json"
    
    bill_info = []
    bill_items = []
    
    def __init__(self):
        self.load_bills()
    
    def create_bill(self, logged_in_user):
        deduct_items_from_inventory = []
        bill = Bill()
        while True:
            print("\nBilling Menu:")
            print("1. Add item to cart")
            print("2. Remove item from cart")
            print("3. Finalize bill")
            print("0. Exit billing")
            choice = input("Enter your choice: ")
            
            if choice == '1':
                bill.add_item_to_cart()
            elif choice == '2':
                bill.remove_item_from_cart()
            elif choice == '3':
                deduct_items_from_inventory = bill.finalize_bill(logged_in_user)
            elif choice == '0':
                break
            else:
                print("Invalid choice. Please try again.")
        if deduct_items_from_inventory:
            return deduct_items_from_inventory
        else:
            return None
    
    def load_bills(self):
        self.bill_info = Bill().data_manager.read_data(self.filenamebillinfo)
        self.bill_items = Bill().data_manager.read_data(self.filenamebillitems)
    
    def view_bills(self):
        print("Viewing all bills:")

        if not self.bill_info:
            self.load_bills()
        
        for bill in self.bill_info:
            print(f"Bill ID: {bill['Bill_id']}, Date: {bill['Date']}, Total Cost: {bill['Total_cost']}")
            for item in self.bill_items:
                if item['Bill_id'] == bill['Bill_id']:
                    print(f"  - Item ID: {item['ID']}, Name: {item['Name']}, Cost: {item['Cost']}, Quantity: {item['Quantity']}")
            print("\n")
            
        print("=========================== \n End of Bills \t Total Bills: ", len(self.bill_info), "\n===========================")
        
    def search_bill(self):
        
        if not self.bill_info:
            self.load_bills()
        
        find_bill_by_id = input("Enter Bill ID to search: ")
        for bill in self.bill_info:
            if bill['Bill_id'] == find_bill_by_id:
                print(f"Bill ID: {bill['Bill_id']}, Date: {bill['Date']}, Total Cost: {bill['Total_cost']}")
                for item in self.bill_items:
                    if item['Bill_id'] == bill['Bill_id']:
                        print(f"  - Item ID: {item['ID']}, Name: {item['Name']}, Cost: {item['Cost']}, Quantity: {item['Quantity']}")
                break
        else:
            print("Bill not found.")
    
    