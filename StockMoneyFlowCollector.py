#!/usr/bin/python3

import pickle
import re
import time

from data.StockMoneyFlow import StockMoneyFlow
from utils import crawler

HOME_DIR = "."

def read_stock_list():
    fi = open(HOME_DIR+"/stock-list.txt", "rb")
    return pickle.load(fi)

if __name__ == "__main__":
    print("get stock money flow start:")

    stock_list = read_stock_list()
    
    stocks_money_flow = []
    for stock in stock_list:
        stock_array = str(stock).split("|")
        stock_symbol = stock_array[0]
        stock_name= stock_array[1]

        info = StockMoneyFlow(stock_symbol, stock_name)
        if info.isValid() and not info.isChuangye():
            stocks_money_flow.append(info)

        if len(stocks_money_flow) > 0 and len(stocks_money_flow)%100 == 0:
            print("Collected money flow number: %d" % len(stocks_money_flow))
            #break
    
    print("total valid stock money flow: %d in %d" % (len(stocks_money_flow), len(stock_list)))

    cur_date = info.opendate
    out = open(HOME_DIR+"/results/moneyflowdata/stock-money-flow-"+cur_date, "wb")
    pickle.dump(stocks_money_flow, out)
    out.close()
        
          
