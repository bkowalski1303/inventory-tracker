class Item:
    def __init__(self, name, stock, restock_threshold):
        self.name = name
        self.stock = stock
        self.restock_threshold = restock_threshold

    def __str__(self):
        return f" {self.name}, {self.stock}, {self.restock_threshold}"
    
    def record_sale(self, quantity):
        self.stock -= quantity
        self.sales_history.append(quantity)