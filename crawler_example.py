import Stockcrawler
import pandas as pd
import twstock
import Quantative_analysis as qa



#read stock file

# stockdf = pd.read_csv('./stocklist/8446_stockinfo.csv')
#
##=======Append and crawler stock info=======================
#stock = Stockcrawler.StockCrawler('1215')
##
#st = stock.AppendStockdf()
#
#print(st)
#

stocklist = pd.read_csv('./stocklist/StockList.csv')
print(stocklist)


stocklist = [2926,2886,6596]

for i in stocklist:
    try :
        stock = Stockcrawler.Stockcrawler(str(i))
        st = stock.AppendStockdf()
    except:
        pass

    time.sleep(3600)
print("crawler done")


##======= Update stocklist to the Last=======================
# Update to the Last stock info
# st = ST.UpdateTotheLast()











