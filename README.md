# prophet
Prophet for money!

# Get stock data:
python3 StockMoneyFlowCollector.py
need code modification HOME_DIR = "/root/prophet"

# Analysis money flow:
python3 StockMoneyFlowStatus.py

# git auto submit setup:
vim ~/.git-credentials
https://{username}:{password}@github.com

git config --global credential.helper store

# crontab setup:
40 11 * * * /root/prophet/autosubmit.sh
20 15 * * * /root/prophet/autosubmit.sh

