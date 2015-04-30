#!/usr/bin/python3

import pickle
import sys
import os
import string

VTP_DAYS = 50
TESTDAYS = 0
TREND1 = 3
TREND2 = 1

open_value = [0]*(VTP_DAYS+TESTDAYS)
high_value = [0]*(VTP_DAYS+TESTDAYS)
low_value = [0]*(VTP_DAYS+TESTDAYS)
close_value = [0]*(VTP_DAYS+TESTDAYS)
volume = [0]*(VTP_DAYS+TESTDAYS)
lj = [0]*(VTP_DAYS+TESTDAYS)
vpt = [0]*(VTP_DAYS+TESTDAYS)

right=0
wrong=0

def read_stock_list():
    fi = open("stock-list.txt", "rb")
    return pickle.load(fi)

def fetch_stock_history(stock_list):
    for s in stock_list:
        if s[0][:2]=="sh":
            yahoo_symbol = s[0][2:]+".ss"
        else:
            yahoo_symbol = s[0][2:]+"."+s[0][:2]
        os.system("wget http://table.finance.yahoo.com/table.csv?s="+yahoo_symbol+" -O /tmp/results/"+s[0])

def loaddata_fromfile(stock):
    global close_value
    global volume

    f = open("/tmp/results/"+stock)
    line_num = 1

    #ignore first line
    line = f.readline()
    line = f.readline()

    while line and line_num<=VTP_DAYS:
        line_array = line.split(",")
        #Date,Open,High,Low,Close,Volume,Adj Close
        close_value[line_num-1] = float(line_array[4])
        volume[line_num-1] = float(line_array[5])

        line_num = line_num + 1
        line = f.readline()

    f.close()

def VPT(stock):
    #http://baike.baidu.com/link?url=CEyz1GzX4fBszDi2cOGjVn5RUal-R51__nXdNFY76BN0LWOCRoFV1YTWs6KTklvzpptBhWSkAc9kDQXSMG3rW_
    global close_value
    global volume
    global right
    global wrong
    buy_flag = 1
    sell_flag = 1

    #not empty file
    if close_value[VTP_DAYS-1] == 0:
        return

    lj[VTP_DAYS-1] = 0
    for j in range(0, VTP_DAYS-1-TESTDAYS):
        i = VTP_DAYS-2-j
        lj[i] = volume[i]/100*(close_value[i]-close_value[i+1])/close_value[i+1]
        vpt[i] = lj[i+1] + lj[i]

    #values in Tr2nd1 all <0 or >0
    for i in range(0, TREND1):
        if vpt[TREND2+i+TESTDAYS] >= 0:
           buy_flag = 0
        if vpt[TREND2+i+TESTDAYS] < vpt[TREND2+i+TESTDAYS+1]:
           buy_flag = 0
       
        if vpt[TREND2+i+TESTDAYS] <= 0:
           sell_flag = 0
        if vpt[TREND2+i+TESTDAYS] > vpt[TREND2+i+TESTDAYS+1]:
           sell_flag = 0
    #values in Trend2 all >0 or <0
    for i in range(0, TREND2):
        if vpt[i+TESTDAYS] <= 0:
           buy_flag = 0
        if vpt[i+TESTDAYS] >= 0:
           sell_flag = 0

    if buy_flag:
        print("\nBUY:"+stock)
        for i in range(0, TREND1+TREND2):
            print(vpt[i+TESTDAYS])
    elif sell_flag:
        print("\nSELL:"+stock)
        for i in range(0, TREND1+TREND2):
            print(vpt[i+TESTDAYS])


    if TESTDAYS > 0:
        if buy_flag:
            if close_value[TESTDAYS-1] > close_value[TESTDAYS]:
                right = right + 1
                print("RIGHT! NEW:"+str(close_value[TESTDAYS-1])+" > OLD:"+str(close_value[1+TESTDAYS]))
            else:
                wrong = wrong + 1
                print("WRONG! NEW:"+str(close_value[TESTDAYS-1])+" < OLD:"+str(close_value[1+TESTDAYS]))
        if sell_flag:
            if close_value[TESTDAYS-1] < close_value[TESTDAYS]:
                right = right + 1
                print("RIGHT! NEW:"+str(close_value[TESTDAYS-1])+" < OLD:"+str(close_value[TESTDAYS]))
            else:
                wrong = wrong + 1
                print("WRONG! NEW:"+str(close_value[TESTDAYS-1])+" > OLD:"+str(close_value[TESTDAYS]))

if __name__ == "__main__":
    stock_list = read_stock_list()

    #download from yahoo
    if len(sys.argv)>=2 and sys.argv[1]=="1":
        fetch_stock_history(stock_list)

    for s in stock_list:
        stock_symbol = s[0]
        if os.path.isfile('/tmp/results/'+stock_symbol):
            loaddata_fromfile(stock_symbol)
            VPT(stock_symbol)

    if TESTDAYS > 0:
        print("right="+str(right))
        print("wrong="+str(wrong))

