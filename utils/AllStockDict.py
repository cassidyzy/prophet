import re
import pickle
from src.common..Constant import ConstantValue

def all_stock_dict():
    stock_dict = {}

    home_dir = ConstantValue.HOME_DIR
    fi = open(home_dir+"stock-list.txt", "rb")
    stock_lines =  pickle.load(fi)
    for s in stock_lines:
        stock_array = str(s).split("|")
        stock_symbol = stock_array[0]
        stock_capital = stock_array[5]
        m = re.search(r"^\w\w300*", stock_symbol)
        if not m:
            stock_dict[stock_symbol] = stock_capital
    return stock_dict

