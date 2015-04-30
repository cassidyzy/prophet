import pickle

def read_stock_list():
    fi = open("stock-list.txt", "wb")
    return pickle.load(fi)