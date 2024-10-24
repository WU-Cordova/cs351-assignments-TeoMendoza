from datastructures.intervaltree import IntervalTree
from dataclasses import dataclass

@dataclass(order = True)
class StockData:
    ticker: str
    name: str
    low: float
    high: float

class StockManager:
    def __init__(self):
        self.stock_tree = IntervalTree()
        stocks = []
        stock_file = open("stocks.txt", "r")
        for line in stock_file:
            stock = line.split(",")
            stocks.append(StockData(stock[0], stock[1], float(stock[2]), float(stock[3])))
        for stock in stocks:
            self.stock_tree.insert(stock.low, stock.high, stock)

    # functions to add, update, and delete stock data
    def add_stock(self, stock: StockData):
        self.stock_tree.insert(stock.low, stock.high, stock)
    def delete_stock(self, stock: StockData): 
        self.stock_tree.delete(stock)
    
    # function for top-K stocks
    def top_k_stocks(self, k: int):
        return self.stock_tree.top_k(k)
    
    # function for bottom-K stocks
    def bottom_k_stocks(self, k: int):
        return self.stock_tree.bottom_k(k)
    
    # function for range query
    def range_query(self, low: float, high: float):
        return self.stock_tree.range_query(low, high)
    

def main():
    stock_manager = StockManager()


if __name__ == "__main__":
    main()