import pickle
import time
import codecs

cur_date = "2015-05-11"

def read_stock_money_flow():
    fi = open("results/moneyflowdata/stock-money-flow-"+cur_date, "rb")
    return pickle.load(fi)

if __name__ == "__main__":
    stock_money_flow_list = read_stock_money_flow()

    file_object = codecs.open("results/moneyflowstatus/"+cur_date+".csv", "w",'gbk')
    output = "symbol,name,moneyflow incoming ratio (%),price change ratio (%),turnover,superbig_angle\n"
    file_object.write(output)

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
#            if symbol == "sz002131":
#                print(str(s))
#                print(str(superbig_volume_in))
#                print(str(superbig_volume_out))
#                print(str(big_volume_in))
#                print(str(big_volume_out))
#                print(str(total_volume))
            output = symbol+","+name+","+str((superbig_volume_in+big_volume_in-superbig_volume_out-big_volume_out)/(total_volume*trade)*100)+","+str(changeratio*100)+","+str(turnover)+","+str(superbig_angle)+"\n"
            file_object.write(output)


    file_object.close( )
