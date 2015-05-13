#!/bin/bash

PYTHON_HOME=/home/weibo/python3
WORK_HOME=/home/weibo/prophet

cd $WORK_HOME
$PYTHON_HOME/bin/python3 StockMoneyFlowCollector.py
git commit -a -m "MOD: update daily money flow data"
git push
