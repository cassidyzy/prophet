import pickle
from data.Constant import ConstantValue

def all_stock_set():
    stock_set = []

    home_dir = ConstantValue.HOME_DIR
    fi = open(home_dir+"stock-list.txt", "rb")
    stock_lines =  pickle.load(fi)
    for s in stock_lines:
        stock_set.append(str(s).split("|")[0])
    return stock_set

