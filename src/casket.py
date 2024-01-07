class Casket:
    def __init__(self, wood_type, length, width, depth):
        self.wood_type = wood_type
        self.length = length
        self.width = width
        self.depth = depth

    def display(self):
        return f"Casket - Wood Type: {self.wood_type}, Length: {self.length}, Width: {self.width}, Depth: {self.depth}"
    
    def calculate_price(self):
        prices = {"Oak": 500, "Mahogany": 600, "Pine": 650, "Walnut": 1000}
        return prices.get(self.wood_type, 0)


caskets = [Casket("Oak", 215, 80, 60), Casket("Mahogany", 215, 80, 60), Casket("Pine", 215, 80, 60), Casket("Walnut", 215, 80, 60)]
# caskets = [...]

