import pickle

from src.common.Constant import ConstantValue

def read_daily_stock_data(cur_date):
    home_dir = ConstantValue.HOME_DIR
    fi = open(home_dir+"results/moneyflowdata/stock-money-flow-"+cur_date, "rb")
    return pickle.load(fi)

def merge_daily_stock_data():

    stocks_dict_set = []

    for cur_date in ConstantValue.DATE_SET:
        stock_money_flow_list = read_daily_stock_data(cur_date)

        stock_dict = {}
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

                big_volume = superbig_volume_in+big_volume_in-superbig_volume_out-big_volume_out
                small_volume = supersmall_volume_in+small_volume_in-supersmall_volume_out-small_volume_out

                add_str = cur_date+"|"+symbol+"|"+name+"|"+str(big_volume)+"|"+str(small_volume)+"|"+str(trade)+"|"+str(changeratio)+"|"+str(total_volume)+"|"+str(turnover)
                stock_dict[symbol] = add_str

        stocks_dict_set.append(stock_dict)

    return stocks_dict_set

