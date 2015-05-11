#!/usr/bin/python3

import pickle
import time
import re

def read_stock_money_flow():
    cur_date = "2015-05-08"
    fi = open("results/moneyflowdata/stock-money-flow-"+cur_date, "rb")
    return pickle.load(fi)

if __name__ == "__main__":
    stock_money_flow_list = read_stock_money_flow()


    print("symbol|name|state|superbig_volume_in|superbig_volume_out|big_volume_in|big_volume_out|small_volume_in|small_volume_out|supersmall_volume_in|supersmall_volume_out|curr_capital|trade|changeratio|total_volume|turnover|superbig_angle")
    for s in stock_money_flow_list:
        stock_array = str(s).split("|")
#        print(stock_array[0])
        m = re.search(r"^\w\w300*", stock_array[0])
        if m:
            print("Chuangye"+str(s))
        #else:
        #    print("Not Chuangye"+str(s))
