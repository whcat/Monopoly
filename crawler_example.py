import Stockcrawler
import pandas as pd
import twstock
import Quantative_analysis as qa



#read stock file

# stockdf = pd.read_csv('./stocklist/8446_stockinfo.csv')

stock = Stockcrawler.StockCrawler('1215')
#

#Append stock info
#
#
st = stock.AppendStockdf()

print(st)


# Update to the Last stock info
# st = ST.UpdateTotheLast()




#
# stockdf.to_csv('./stocklist/2330_stockinfo.csv')

# alist = list(stockdf["date"])
#
# for i,e in enumerate(stockdf[date]):
#     alist[i] = e.split(" ")[0]
#

# print(alist)
# print(list(stockdf['turnover']))
# print(stockdf)








