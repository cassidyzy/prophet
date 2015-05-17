import pickle
import time
import codecs
import sys

from data.Constant import ConstantValue
from utils import AllStockSet
from utils import StockDailyMerge
from utils import AvgData

def output_bigin_smallout_foralldays():

    selected_symbol_set = []
    if stock_custom_set == "" or stock_custom_set == "all":
        # get all availabile stock symbols
        selected_symbol_set = AllStockSet.all_stock_set()
    else:
        # get custom stock list
        file_read = open(home_dir+stock_custom_set, "r")
        for line in file_read.readlines():
            selected_symbol_set.extend(line.split())

        file_read.close()
        
    #total volume and price change for all days
    volume_per_price = {}

    print("symbol\t\tname\t\tbig (%)\tsmall (%)\tprice (%)\tturnover\tbig/price")

    for stock in selected_symbol_set:
        if stock not in avg_data_dict:
            continue

        total_big_volume_in = 0
        total_small_volume_in = 0
        total_price_change = 0

        for i in range(0, day_num):
            d = stocks_dict_set[i]
            if not stock in d:
                continue
            result_array = d[stock].split("|")
            total_big_volume_in = total_big_volume_in + float(result_array[3])
            total_small_volume_in = total_small_volume_in + float(result_array[4])
            trade_value = float(result_array[5])
            total_price_change = total_price_change + float(result_array[6])

        avg_volume = float(avg_data_dict[stock].split("|")[1])
        if trade_value==0 or avg_volume==0:
            continue

        key_value = "%s|%s|%s|%s|%s|%s" % (result_array[1], result_array[2], str(round(total_big_volume_in/trade_value/avg_volume*100, 2)), str(round(total_small_volume_in/trade_value/avg_volume*100, 2)), str(round(total_price_change*100,2)), str(result_array[8]))

        if output_num == 0:
            #no filter set, print all money flow info
            volume_per_price[key_value] = 1
        elif (total_big_volume_in > 0 and total_price_change > 0):
            volume_per_price[key_value] = round(total_big_volume_in/trade_value/avg_volume/total_price_change, 2)
        elif (total_big_volume_in > 0 and total_price_change <= 0):
            volume_per_price[key_value] = 9999

    num = 0
    for item in sorted(volume_per_price.items(), key=lambda d: d[1], reverse=True):
        output_array = item[0].split("|")
        output_str = output_array[0]+"\t"+output_array[1]+"  \t"+output_array[2]+"%\t"+output_array[3]+"%\t\t"+output_array[4]+"%\t\t"+output_array[5]+"\t\t"+str(item[1])
#        if stock_custom_set == "":
#            file_output_str = output_array[0]+","+output_array[1]+","+output_array[2]+","+output_array[3]+","+output_array[4]+","+output_array[5]+","+str(item[1])+"\n"
#            file_object.write(file_output_str)
        num = num + 1
        if output_num ==0 or num <= output_num:
            print(output_str)


if __name__ == "__main__":

    cur_date_set = ConstantValue.DATE_SET
    home_dir = ConstantValue.HOME_DIR

    #default all stocks
    stock_custom_set = ""
    #default no filter, list all results
    output_num = 0
    #default days
    day_num = 1

    if len(sys.argv)>=4:
        stock_custom_set = sys.argv[1]
        day_num = int(sys.argv[2])
        output_num = int(sys.argv[3])
    if len(sys.argv)>=3:
        stock_custom_set = sys.argv[1]
        day_num = min(len(cur_date_set), int(sys.argv[2]))
    elif len(sys.argv)>=2:
        stock_custom_set = sys.argv[1]

    #get all stock data for all days
    stocks_dict_set = StockDailyMerge.merge_daily_stock_data()
    #get average data for each stock
    avg_data_dict = AvgData.MA20_values(stocks_dict_set)

#    for i in range(0, day_num):
#        stocks_dict_set.append(stock_money_flow_status(cur_date_set[i]))

#    if stock_custom_set == "":
#        file_object = codecs.open(home_dir+"results/moneyflowstatus/"+cur_date_set[0]+".csv", "w",'gbk')
#        output = "symbol,name,big in(%),small in(%),price(%),turnover,big/price\n"
#        file_object.write(output)

    #make average volume for every stock
    output_bigin_smallout_foralldays()

#    if stock_custom_set == "":
#        file_object.close()
