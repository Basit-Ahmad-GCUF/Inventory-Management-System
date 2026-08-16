
class BillItem:
    def __init__(self, id, name, cost, quantity):
        self.id = id
        self.name = name
        self.cost = cost
        self.quantity = quantity
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "cost": self.cost,
            "quantity": self.quantity,
        }
    
    def from_dict(self, data):
        self.id = data.get("id", self.id)
        self.name = data.get("name", self.name)
        self.cost = data.get("cost", self.cost)
        self.quantity = data.get("quantity", self.quantity)  