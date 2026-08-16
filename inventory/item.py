
class Item:
    def __init__(self, id, name, cost, quantity, description, entry_date, expiration_date):
        self.id = id
        self.name = name
        self.cost = cost
        self.quantity = quantity
        self.description = description
        self.entry_date = entry_date
        self.expiration_date = expiration_date
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "cost": self.cost,
            "quantity": self.quantity,
            "description": self.description,
            "entry_date": self.entry_date,
            "expiration_date": self.expiration_date
        }
    
    def from_dict(self, data):
        self.ID = data.get("id", self.id)
        self.name = data.get("name", self.name)
        self.cost = data.get("cost", self.cost)
        self.quantity = data.get("quantity", self.quantity)
        self.description = data.get("description", self.description)
        self.entry_date = data.get("entry_date", self.entry_date)
        self.expiration_date = data.get("expiration_date", self.expiration_date)
        