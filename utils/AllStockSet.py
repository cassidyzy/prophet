import re
import pickle
from data.Constant import ConstantValue

def all_stock_set():
    stock_set = []

    home_dir = ConstantValue.HOME_DIR
    fi = open(home_dir+"stock-list.txt", "rb")
    stock_lines =  pickle.load(fi)
    for s in stock_lines:
        stock_symbol = str(s).split("|")[0]
        m = re.search(r"^\w\w300*", stock_symbol)
        if not m:
            stock_set.append(stock_symbol)
    return stock_set

