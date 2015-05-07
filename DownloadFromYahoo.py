import pickle
import os
import sys
import urllib.request
import string
import threading
from time import sleep

THREAD_NUMBER = 1
    
def read_stock_list():
    fi = open("stock-list.txt", "rb")
    return pickle.load(fi)

def fetch_stock_history(start_num,end_num):
    for stock_line in stock_list[start_num:end_num]:
        s = str(stock_line).split("|")
        if s[0][:2]=="sh":
            yahoo_symbol = s[0][2:]+".ss"
        else:
            yahoo_symbol = s[0][2:]+"."+s[0][:2]
        url = "http://table.finance.yahoo.com/table.csv?s="+yahoo_symbol
        print("Downloading "+s[0]+" ...")
        urllib.request.urlretrieve(url, "C:\\05. Stock\\results\\"+s[0])
        #sleep(1)


stock_list = read_stock_list()
threads = []

if __name__ == "__main__":
    
    for i in range(0, THREAD_NUMBER):
        start_num = int(i*len(stock_list)/THREAD_NUMBER)
        end_num = int((i+1)*len(stock_list)/THREAD_NUMBER - 1)
        
        t = threading.Thread(target=fetch_stock_history,args=(start_num,end_num))
        threads.append(t)

    for t in threads:
        t.setDaemon(True)
        t.start()
        
