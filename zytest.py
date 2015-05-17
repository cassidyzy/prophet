from utils import StockDailyMerge
from utils import AvgData




if __name__ == "__main__":
    result = AvgData.MA5_values(StockDailyMerge.merge_daily_stock_data())
    print(result['sh603222'])
    result = AvgData.MA20_values(StockDailyMerge.merge_daily_stock_data())
    print(result['sh603222'])
