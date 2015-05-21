import pickle
import time
import codecs
import sys

from src.common.Constant import ConstantValue
from src.data import AllStockDict
from src.compute import StockDailyMerge
from src.compute import AvgData

def find_mnht1_stocks():
        
    for stock in selected_symbol_set:

        day_num = min(10, len(cur_date_set)-1)
        MNHT1_flag = 0
        min_price = 50000
        stock_price_set = []
        stock_volume_set = []


        for i in range(0, day_num):
            d = stocks_dict_set[i]
            d_before = stocks_dict_set[i+1]
            if not stock in d or not stock in d_before:
                break

            result_array = d[stock].split("|")
            result_array_before = d_before[stock].split("|")

            stock_name = result_array[2]
            stock_price = float(result_array[5])
            stock_price_set.append(stock_price)
            if i == 0:
                current_price = stock_price

            stock_price_change = float(result_array[6])*100
            stock_volume = float(result_array[7])
            stock_volume_set.append(stock_volume)

            stock_volume_before = float(result_array_before[7])

            if i >=2 and stock_price_change >=9.8 and stock_price*0.9 < min_price:
                MNHT1_flag = 1
                break

            if stock_price < min_price:
                min_price = stock_price

            if stock_volume_before < stock_volume:
                break

            if stock_price_change > 0:
                break

        if MNHT1_flag == 1:
            total_capital = int(int(all_stock_dict[stock])*stock_price/100000000)
            if total_capital > 100 or current_price > 20:
                continue
            print("MNHT1: %s %s %d" % (stock, stock_name, total_capital))
            print(stock_price_set)
            print(stock_volume_set)
            print("\n")



def find_mnht2_stocks():

    for stock in selected_symbol_set:

        day_num = min(10, len(cur_date_set)-1)
        MNHT2_flag = 0
        min_price = 50000
        stock_price_set = []
        stock_volume_set = []
        curret_price = 50000

        for i in range(0, day_num):
            d = stocks_dict_set[i]
            d_before = stocks_dict_set[i+1]
            if not stock in d or not stock in d_before:
                break

            result_array = d[stock].split("|")
            result_array_before = d_before[stock].split("|")

            stock_name = result_array[2]
            stock_price = float(result_array[5])
            if i == 0:
                current_price = stock_price

            stock_price_set.append(stock_price)

            stock_price_change = float(result_array[6])*100
            stock_volume = float(result_array[7])
            stock_volume_set.append(stock_volume)

            stock_volume_before = float(result_array_before[7])

            if i >=3 and stock_volume > stock_volume_before*2 and stock_price_change > 0 and stock_price < min_price and stock_price*1.05 > current_price:
                stock_volume_set.append(stock_volume_before)
                MNHT2_flag = 1
                break

            if stock_price < min_price:
                min_price = stock_price


        if MNHT2_flag == 1:
            total_capital = int(int(all_stock_dict[stock])*stock_price/100000000)
            if total_capital > 100 or current_price > 20:
                continue
            print("MNHT2: %s %s %d" % (stock, stock_name, total_capital))
            print(stock_price_set)
            print(stock_volume_set)
            print("\n")


def find_mnht3_stocks():

    for stock in selected_symbol_set:

        day_num = len(cur_date_set)
        MNHT3_flag = 0
        min_price = 50000
        max_price = 0
        stock_price_set = []
        stock_volume_set = []

        for i in range(0, day_num):
            d = stocks_dict_set[i]
            if not stock in d:
                break

            result_array = d[stock].split("|")

            stock_name = result_array[2]
            stock_price = float(result_array[5])
            stock_price_change = float(result_array[6])*100
            stock_volume = float(result_array[7])

            if stock_price < min_price:
                min_price = stock_price

            if stock_price > max_price:
                max_price = stock_price

            avg_volume = float(avg_data_dict[stock].split("|")[1])

            if i <= 1 and stock_volume > avg_volume*2 and stock_price_change > 0:
                MNHT3_flag = 1

            if i > 1 and stock_volume > avg_volume*1.05:
                MNHT3_flag = 0

        if max_price/min_price > 1.2:
            MNHT3_flag = 0

        if MNHT3_flag == 1:
            total_capital = int(int(all_stock_dict[stock])*stock_price/100000000)
            if total_capital > 100:
                continue
            print("MNHT3: %s %s %d" % (stock, stock_name, total_capital))


if __name__ == "__main__":

    cur_date_set = ConstantValue.DATE_SET
    home_dir = ConstantValue.HOME_DIR
    max_capital = ConstantValue.COMPANY_DAPITAL_SIZE

    #get all stock data for all days
    stocks_dict_set = StockDailyMerge.merge_daily_stock_data()
    avg_data_dict = AvgData.MA55_values(stocks_dict_set)

    all_stock_dict = AllStockDict.all_stock_dict()
    selected_symbol_set = all_stock_dict.keys()

    find_mnht1_stocks()
    find_mnht2_stocks()
#    find_mnht3_stocks()

