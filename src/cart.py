from src.casket import Casket
from src.tombstone import Tombstone
from src.urn import Urn

class Cart:
    def __init__(self):
        self.items = []

    def add_item(self, item):
        self.items.append(item)

    def calculate_price(self):
        total_price = 0
        for item in self.items:
            if isinstance(item, Casket):
                total_price += item.calculate_price()
            elif isinstance(item, Tombstone):
                total_price += item.calculate_price()
            elif isinstance(item, Urn):
                total_price += item.calculate_price()
        return total_price
    
cart = Cart()
