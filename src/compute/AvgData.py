import pickle

from src.common.Constant import ConstantValue
from src.data import AllStockDict
from src.compute import StockDailyMerge

stock_set = AllStockDict.all_stock_dict().keys()

def avg_values(stocks_dict_set, avg_day_num):

    avg_dict = {}
    day_num = min(avg_day_num, len(ConstantValue.DATE_SET))

    for stock in stock_set:
        total_price = 0
        total_volume = 0
        fail_day_num = 0

        for i in range(0, day_num):
            oneday_stock_dict = stocks_dict_set[i]
            if not stock in oneday_stock_dict:
                fail_day_num = fail_day_num + 1
                continue

            result_array = oneday_stock_dict[stock].split("|")
            total_price = total_price + float(result_array[5])
            total_volume = total_volume + float(result_array[7])

        valid_day_num = day_num-fail_day_num
        if valid_day_num > 0:
            avg_str = str(total_price/valid_day_num)+"|"+str(total_volume/valid_day_num)
            avg_dict[stock] = avg_str

    return avg_dict

def MA5_values(stocks_dict_set):
    return avg_values(stocks_dict_set, ConstantValue.MA5_DAYS)

def MA10_values(stocks_dict_set):
    return avg_values(stocks_dict_set, ConstantValue.MA10_DAYS)

def MA20_values(stocks_dict_set):
    return avg_values(stocks_dict_set, ConstantValue.MA20_DAYS)

def MA30_values(stocks_dict_set):
    return avg_values(stocks_dict_set, ConstantValue.MA30_DAYS)

def MA55_values(stocks_dict_set):
    return avg_values(stocks_dict_set, ConstantValue.MA55_DAYS)

