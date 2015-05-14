#!/bin/bash

HOME=/home/weibo
PYTHON_HOME=$HOME/python3
WORK_HOME=$HOME/prophet

sh $HOME/.bash_profile

cd $WORK_HOME
git pull --rebase
$PYTHON_HOME/bin/python3 StockMoneyFlowCollector.py
git add results
git commit -m "MOD: update daily money flow data"
git push
