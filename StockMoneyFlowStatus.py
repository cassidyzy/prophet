import pickle
import time
import codecs
import sys

from data.Constant import ConstantValue

OUTPUT_NUM = 30

def read_stock_money_flow(cur_date):
    fi = open("results/moneyflowdata/stock-money-flow-"+cur_date, "rb")
    return pickle.load(fi)

def stock_money_flow_status(cur_date):

    return_dict = {}

    stock_money_flow_list = read_stock_money_flow(cur_date)

    for s in stock_money_flow_list:
        money_flow_array = str(s).split("|")
        symbol = money_flow_array[0]
        name = money_flow_array[1]
        state = money_flow_array[2]
        superbig_volume_in = float(money_flow_array[3])
        superbig_volume_out = float(money_flow_array[4])
        big_volume_in = float(money_flow_array[5])
        big_volume_out = float(money_flow_array[6])
        small_volume_in = float(money_flow_array[7])
        small_volume_out = float(money_flow_array[8])
        supersmall_volume_in = float(money_flow_array[9])
        supersmall_volume_out = float(money_flow_array[10])
        curr_capital = float(money_flow_array[11])
        trade = float(money_flow_array[12])
        changeratio = float(money_flow_array[13])
        total_volume = float(money_flow_array[14])
        turnover = float(money_flow_array[15])
        superbig_angle = float(money_flow_array[16])

        if state == "1" and total_volume > 0:

            big_volume_ratio = (superbig_volume_in+big_volume_in-superbig_volume_out-big_volume_out)/(total_volume*trade)*100
            small_volume_ratio = (supersmall_volume_in+small_volume_in-supersmall_volume_out-small_volume_out)/(total_volume*trade)*100

            add_str = cur_date+"|"+symbol+"|"+name+"|"+str(round(big_volume_ratio,1))+"|"+str(round(small_volume_ratio,1))+"|"+str(round(changeratio*100,2))+"|"+str(turnover)
            return_dict[symbol] = add_str

    return return_dict


def output_bigin_smallout_foralldays(stocks_dict_set):

    # get all availabile stock symbols
    selected_symbol_set = stocks_dict_set[0].keys()
    for d in stocks_dict_set:
        selected_symbol_set = selected_symbol_set & d.keys()

    #total volume and price change for all days
    volume_per_price = {}

    print("symbol\t\tname\t\tbig (%)\tsmall (%)\tprice (%)\tbig/price\tturnover")
    for stock in selected_symbol_set:
        total_big_volume_in = 0
        total_small_volume_in = 0
        total_price_change = 0

        for d in stocks_dict_set:
            result_array = d[stock].split("|")
            total_big_volume_in = total_big_volume_in + float(result_array[3])
            total_small_volume_in = total_small_volume_in + float(result_array[4])
            total_price_change = total_price_change + float(result_array[5])

        if total_big_volume_in > 0 and total_price_change > 0:
            key_value = "%s|%s|%s|%s|%s|%s" % (result_array[1], result_array[2], str(round(total_big_volume_in, 2)), str(round(total_small_volume_in, 2)), str(round(total_price_change,2)), str(result_array[6]))
            volume_per_price[key_value] = round(total_big_volume_in/total_price_change, 2)

    num = 0
    for item in sorted(volume_per_price.items(), key=lambda d: d[1], reverse=True):
        output_array = item[0].split("|")
        output_str = output_array[0]+"\t"+output_array[1]+"  \t"+output_array[2]+"%\t"+output_array[3]+"%\t\t"+output_array[4]+"%\t\t"+output_array[5]+"\t\t"+str(item[1])
        file_output_str = output_array[0]+","+output_array[1]+","+output_array[2]+","+output_array[3]+","+output_array[4]+","+output_array[5]+","+str(item[1])+"\n"
        file_object.write(file_output_str)
        num = num + 1
        if num <= OUTPUT_NUM:
            print(output_str)


if __name__ == "__main__":

    cur_date_set = ConstantValue.date_set

    stocks_dict_set = []

    for i in range(0, len(cur_date_set)):
        stocks_dict_set.append(stock_money_flow_status(cur_date_set[i]))

    file_object = codecs.open("results/moneyflowstatus/"+cur_date_set[0]+".csv", "w",'gbk')
    output = "symbol,name,big in(%),small in(%),price(%),big/price,turnover\n"
    file_object.write(output)

    output_bigin_smallout_foralldays(stocks_dict_set)

    file_object.close()
