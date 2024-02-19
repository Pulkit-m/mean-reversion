import baostock as bs
import pandas as pd
from tqdm import tqdm
import os

DATA_START_DATE_INSAMPLE = '2022-04-01' 
DATA_END_DATE_INSAMPLE = '2022-06-30'
DATA_START_DATE_OUTSAMPLE = '2022-07-01' 
DATA_END_DATE_OUTSAMPLE = '2022-07-31'
FREQUENCY = "30"   #30 for 30min, 60 for 60min, d for day, m for month, and so on 
ADJUSTFLAG = "3"   # default value for no adjustment. 

if(not os.path.exists("./data/raw/insample")): 
    os.makedirs("./data/raw/insample", exist_ok=True)
if(not os.path.exists("./data/raw/outsample")): 
    os.makedirs("./data/raw/outsample", exist_ok=True)

# import os 
# print(os.listdir())
indexStocksDf = pd.read_csv('./data/raw/csi500_index_composition.csv', index_col=None, encoding='gbk') 
print(indexStocksDf.head())


lg = bs.login()
print('login respond error_code:'+lg.error_code)
print('login respond  error_msg:'+lg.error_msg)
for stock in tqdm(indexStocksDf.code): 
    stock_ticker = '-'.join(stock.split('.'))
    # insample data download
    rs = bs.query_history_k_data_plus(stock,
        "date,time,code,open,high,low,close,volume,amount,adjustflag",
        start_date=DATA_START_DATE_INSAMPLE, end_date=DATA_END_DATE_INSAMPLE,
        frequency=FREQUENCY, adjustflag=ADJUSTFLAG)
    print('query_history_k_data_plus respond error_code:'+rs.error_code)
    print('query_history_k_data_plus respond  error_msg:'+rs.error_msg) 

    data_list = []
    while (rs.error_code == '0') & rs.next():
        data_list.append(rs.get_row_data())
    result = pd.DataFrame(data_list, columns=rs.fields) 
    result.rename(columns = str.capitalize, inplace=True) 
    result.to_csv(f"./data/raw/insample/history_stock_{stock_ticker}.csv", index=False)
    
    # outsample data download
    rs = bs.query_history_k_data_plus(stock,
        "date,time,code,open,high,low,close,volume,amount,adjustflag",
        start_date=DATA_START_DATE_OUTSAMPLE, end_date=DATA_END_DATE_OUTSAMPLE,
        frequency=FREQUENCY, adjustflag=ADJUSTFLAG)
    print('query_history_k_data_plus respond error_code:'+rs.error_code)
    print('query_history_k_data_plus respond  error_msg:'+rs.error_msg) 

    data_list = []
    while (rs.error_code == '0') & rs.next():
        data_list.append(rs.get_row_data())
    result = pd.DataFrame(data_list, columns=rs.fields) 
    result.rename(columns = str.capitalize, inplace=True) 
    result.to_csv(f"./data/raw/outsample/history_stock_{stock_ticker}.csv", index=False)
