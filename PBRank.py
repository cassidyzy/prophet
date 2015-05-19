import StockListReader

if __name__ == "__main__":
    stocks = StockListReader.read_stock_list()
    money_flows = StockListReader.read_cur_money_flow()
    pb = []
    for stock in stocks:
        if stock.symbol not in money_flows:
            continue
        money_flow = money_flows[stock.symbol]
        if money_flow.isChuangye() or stock.net_estate == 0:
            continue
        pb.append((stock, money_flow.trade / stock.net_estate, money_flow))
    pb = sorted(pb, key=lambda k : k[1])
    for s in pb:
        if s[1] > 0:
            print("%s\t%f\t%s(%s,%s)" % (s[0].symbol, s[1], s[0].name, s[0].net_estate, s[2].trade))