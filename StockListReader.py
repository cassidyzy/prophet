import pickle

def read_stock_list():
    fi = open("stock-list.txt", "rb")
    return pickle.load(fi)

if __name__ == "__main__":
    stock_list = read_stock_list()
    for s in stock_list:
        print(s)
