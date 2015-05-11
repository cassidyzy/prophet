import re

from utils import crawler


class StockBasicInfo:
    def __init__(self, symbol, name):
        print("init %s" % symbol)
        self.symbol = symbol
        self.name = name
        self.state = 0
        self._crawl4Attrs(symbol)
    
    def _crawl4Attrs(self, symbol):
        url = "http://finance.sina.com.cn/realstock/company/%s/nc.shtml" % symbol
        html = crawler.crawl(url)
        if html is None:
            return
        # state
        state = self._reg4Value(html, "stock_state")
        if state is not None:
            self.state = int(state)
        # net_estate
        net_estate = self._reg4Value(html, "mgjzc")
        if net_estate is not None:
            self.net_estate = float(net_estate)
        # profit_per_stock
        profit_per_stock = self._reg4Value(html, "fourQ_mgsy")
        if profit_per_stock is not None:
            self.profit_per_stock = float(profit_per_stock) 
    
    def _reg4Value(self, html, key):
        m = re.search(r"var %s ?= ?([^;]*?);" % key, html)
        if m:
            return m.group(1)
        else:
            return None
    
    def isValid(self):
        return self.state == 1
        
    def __str__(self):
        return "%s|%s|%s|%s|%s" % (self.symbol, self.name, self.state, self.net_estate, self.profit_per_stock)
