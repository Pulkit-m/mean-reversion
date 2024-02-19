# import os 
# os.listdir()

import baostock as bs
import pandas as pd

lg = bs.login()
print('login respond error_code:'+lg.error_code)
print('login respond  error_msg:'+lg.error_msg)

rs = bs.query_zz500_stocks(date = '2021-01-01')
print('query_zz500 error_code:'+rs.error_code)
print('query_zz500  error_msg:'+rs.error_msg)

zz500_stocks = []
while (rs.error_code == '0') & rs.next():
    zz500_stocks.append(rs.get_row_data())
result = pd.DataFrame(zz500_stocks, columns=rs.fields)
result.to_csv("./data/raw/csi500_index_composition.csv", encoding="gbk", index=False)
print(result)

bs.logout()
