from data.datamanager import Data_Manager

class Billing_Manager:
    def __init__(self, DB: Data_Manager):
        self.database = DB
        
    def add_bill(self, bill_id, biller, datetime_str, total_cost, bill_items_list) -> None:
        self.database.add_bill(bill_id, biller, datetime_str, total_cost, bill_items_list)
    
    def get_bill_with_id(self, bill_id) -> dict:
        Bill = self.database.get_bill_by_id(bill_id)
        Bill["bill_items"] = self.database.get_bill_items(bill_id)
        
        return Bill