from data.datamanager import Data_Manager

class Billing_Manager:
    def __init__(self, database: Data_Manager):
        self.db = database
    
    def add_bill(self, bill_id, biller, datetime_str, total_cost, bill_items_list) -> None:
        # 1. Insert main bill info
        bill_query = "INSERT INTO bill (bill_id, biller, datetime, total_cost) VALUES (?, ?, ?, ?)"
        self.db.execute(bill_query, (bill_id, biller, datetime_str, total_cost))

        # 2. Insert all items associated with this bill
        item_query = "INSERT INTO bill_items (bill_id, item_id, name, cost, quantity, subtotal) VALUES (?, ?, ?, ?, ?, ?)"
        for item_id, name, cost, qty, subtotal in bill_items_list:
            self.db.execute(item_query, (bill_id,item_id, name, cost, qty, subtotal))

    def get_all_bills(self):
        return self.db.fetch_all("SELECT * FROM bill")

    def get_bill_items(self, bill_id):
        return self.db.fetch_all("SELECT * FROM bill_items WHERE bill_id = ?", (bill_id,))

    def get_bill_by_id(self, bill_id):
        return self.db.fetch_one(
            "SELECT * FROM bill WHERE bill_id = ?", (bill_id,)
        )
        
        
    def get_bill_with_id(self, bill_id) -> dict:
        Bill = self.get_bill_by_id(bill_id)
        Bill["bill_items"] = self.get_bill_items(bill_id)    
        
        return Bill
    
    def get_daily_top_items(self, date_str):
        query = """
                SELECT name, SUM(quantity)
                FROM bill_items
                JOIN bill on bill_items.bill_id = bill.bill_id
                WHERE DATE(bill.datetime) = ?
                GROUP BY name
                ORDER BY SUM(quantity) DESC
                LIMIT 10
                """
        return self.db.fetch_all(query, (date_str,))
    
    def get_top_items(self, start_date_str, end_date_str):
        query = """
                SELECT name, SUM(quantity)
                FROM bill_items
                JOIN bill on bill_items.bill_id = bill.bill_id
                WHERE DATE(bill.datetime) BETWEEN ? AND ?
                GROUP BY name
                ORDER BY SUM(quantity) DESC
                LIMIT 10
                """
        return self.db.fetch_all(query, (start_date_str, end_date_str))
    
    def get_revenue_between_dates(self, start_date_str, end_date_str):
        query = "SELECT SUM(total_cost) FROM bill WHERE DATE(datetime) BETWEEN ? AND ?"
        result = self.db.fetch_one(query, (start_date_str, end_date_str))
        revenue = result[0] if result[0] is not None else 0
        return revenue
    
    def count_bills_between_dates(self, start_date_str, end_date_str):
        query = "SELECT COUNT(*) FROM bill WHERE DATE(datetime) BETWEEN ? AND ?"
        result = self.db.fetch_one(query, (start_date_str, end_date_str))
        count = result[0] if result[0] is not None else 0
        return count