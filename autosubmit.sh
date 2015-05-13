#!/bin/bash

HOME=/home/weibo
PYTHON_HOME=$HOME/python3
WORK_HOME=$HOME/prophet

sh $HOME/.bash_profile

cd $WORK_HOME
$PYTHON_HOME/bin/python3 StockMoneyFlowCollector.py
git commit -a -m "MOD: update daily money flow data"
git push
