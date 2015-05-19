#!/usr/bin/python3

import datetime
import os
import pickle
import re


def read_stock_list():
    fi = open("stock-list.txt", "rb")
    return pickle.load(fi)

def read_cur_money_flow():
    data_dir = "results/moneyflowdata"
    # get most recent date
    max_date = None
    for fn in os.listdir(data_dir):
        m = re.match(r'stock-money-flow-(.*)', fn)
        if m:
            d = datetime.datetime.strptime(m.group(1), '%Y-%m-%d')
            if max_date is None:
                max_date = d
                selected = fn
            else:
                if d > max_date:
                    max_date = d
                    selected = fn
    if selected is None:
        print("sb le!, please quit!")
        return None
    
    # read data in map, key is symbol, value is obj
    result = {}
    l = pickle.load(open("%s/%s" % (data_dir, selected), "rb"))
    for s in l:
        result[s.symbol] = s
    return result
