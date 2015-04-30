#!/usr/bin/python3

import pickle
import re
import urllib.request


def crawl_stock_info(url):
    response = urllib.request.urlopen(url)
    html = str(response.read(), "gbk")
    pattern = re.compile(r'symbol:"([^"]*)",code:"[^"]*",name:"([^"]*)"')
    l = []
    for m in pattern.finditer(html):
        l.append((m.group(1), m.group(2)))
    return l
    

if __name__ == "__main__":
    print("update stock list start:")
    sina_stock_list_url = "http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getHQNodeData?page=%d&num=%d&sort=symbol&asc=1&node=hs_a&symbol=&_s_r_a=page"
    page_size = 80
    stock_list = []
    for i in range(1, 100):
        print("processing sina stock list %d" % i)
        l = crawl_stock_info(sina_stock_list_url % (i, page_size))
        if len(l) > 0:
            stock_list.extend(l)
        if len(l) < page_size:
            break
    print("total stock count:%d" % len(stock_list))
    out = open("stock-list.txt", "wb")
    pickle.dump(stock_list, out)
    out.close()
        
          
