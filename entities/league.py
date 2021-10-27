class League():
    def __init__(self, id: int, name: str, quantity: int=20): 
        self.id = id
        self.name = name
        self.quantity = quantity
    def __repr__(self):
        return f"League('{self.name}', '{self.quantity}')"

    def get_as_json(self):
        return {
                "id": self.id,
                "name": self.name,
                "quantity": self.quantity
            }
