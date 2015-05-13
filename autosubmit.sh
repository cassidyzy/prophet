#!/bin/bash
/usr/bin/python3 /root/prophet/StockMoneyFlowCollector.py
git commit -a -m "MOD: update daily money flow data"
git push
