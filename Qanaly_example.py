import pandas as pd
import Quantative_analysis as qa

stockdf = pd.read_csv('./stocklist/1215_stockinfo.csv',index_col = "date")

#print(stockdf)

qa = qa.Techanaly(stockdf)


# 簡單移動平均數
#sma = qa.smaCal(5)
#
#print("移動平均五日數:",sma)
#
#print("==="*4,"簡單移動平均數","==="*4)
#===========================================================
##加權移動平均數
#wma = qa.wmaCal([0.2,0.3,0.5])
#
#print(wma)
#
#print("==="*4,"加權移動平均數","==="*4)
#===========================================================
##指數加權移動平均數
#ewma = qa.ewmaCal(5,0.3)
#
#print(ewma)
#
#print("==="*4,"指數加權移動平均數","==="*4)
#===========================================================
## DIFF value
#diff = qa.DIFF()
#print(diff)
#
#print("==="*4,"DIFF value","==="*4)
#===========================================================
##DEA value
#dea = qa.DEA()
#print("==="*4,"DEA value","==="*4)
#===========================================================
##MACD value
#macd = qa.MACD()
#print(macd)
#print("==="*4,"MACD value","==="*4)
#===========================================================
##RSV value
#rsv = qa.RSV(5)
#print(rsv)
#
#print("==="*4,"RSV value","==="*4)
#===========================================================
# K value
kvalue = qa.Kvalue()
#print(kvalue)
#
#print("==="*4,"K value","==="*4)
#rsv = qa.RSV(5)
##print(type(rsv))
#print(qa.Kvalue(2/3,1/3,rsv))
#===========================================================
#D value
#dvalue = qa.Dvalue()
#print(dvalue)
#print("==="*4),"D value","==="*4)
#===========================================================
#J value
jvalue = qa.Jvalue()

print(jvalue)
#
#print("==="*4,"J value","==="*4)
#===========================================================
##KDJ value
#
#kdj = qa.KDJvalue()
#print(kdj)
#
#print("==="*4,"KDJ value","==="*4)



