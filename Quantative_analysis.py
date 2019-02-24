import numpy as np
import pandas as pd

class Techanaly():

    def __init__(self,stockdf):
        self.stockdf = stockdf
        self.stPrice = pd.Series(stockdf['close'],index=stockdf.index)
        self.CLOSE = pd.Series(stockdf['close'],index=stockdf.index)
        self.High = pd.Series(stockdf['high'],index=stockdf.index)
        self.LOW = pd.Series(stockdf['low'],index=stockdf.index)
        self.OPEN = pd.Series(stockdf['open'],index=stockdf.index)


    #簡單移動平均數
    def smaCal(self,days:int):
        sma = pd.Series([np.nan] * len(self.stPrice), index=self.stPrice.index)
        for i in range(days-1,len(self.stPrice)):
            sma[i] = np.mean(self.stPrice[i-days+1:i+1])
        return sma

    #簡單移動平均數生成器
    def sma_generator(self, days : int):
        for i in range(days-1, len(self.stPrice)):
            sma_g = np.mean(self.stPrice[i - days + 1:i + 1])
            yield sma_g

    #加權移動平均數
    def wmaCal(self, weights : list): # weights = [前n天的權重,前n-1天的權重,....,當天的權重]
        wma = pd.Series([np.nan] * len(self.stPrice), index=self.stPrice.index)
        lenW = len(weights)

        for i in range(lenW-1, len(self.stPrice)):
            wma[i] = sum(map(lambda x: x[0]*x[1], zip(self.stPrice[i - lenW + 1:i + 1], weights)))
        return wma

    #加權移動平均數生成器
    def wma_generator(self, weights:list):# weights = [前n天的權重,前n-1天的權重,....,當天的權重]
        lenW = len(weights)
        for i in range(lenW-1, len(self.stPrice)):
            wma_g = sum(map(lambda x: x[0]*x[1], zip(self.stPrice[i - lenW + 1:i + 1], weights)))
            yield wma_g

    #指數加權移動平均數
    def ewmaCal(self, period:int, exponential:float()):
        ewma = pd.Series([np.nan] * len(self.stPrice), index=self.stPrice.index)
        ewma[period-1]=np.mean(self.stPrice[0:period])

        for i in range(period, len(self.stPrice)):
            ewma[i]= exponential * self.stPrice[i] + (1 - exponential) * ewma[i - 1]
        return ewma

    #指數加權移動平均生成器
    def ewma_generator(self, period:int, exponential:float()):
        for i in range(period-1, len(self.stPrice)):
            if i == period -1:
                ewma_g = np.mean(self.stPrice[0:period])
            else:
                ewma_g = exponential * self.stPrice[i] + (1 - exponential) * ewma_g

            yield ewma_g

    def DIFF(self,fastline=12,slowline=26):#預設 slowline = EMA26,fastline = EMA12
        ExpofSlow = 2/(slowline+1)
        ExpofFast = 2/(fastline+1)

        diff = self.ewmaCal(fastline,ExpofFast) - self.ewmaCal(slowline,ExpofSlow)

        return diff.dropna()


    def DEA(self,fastline=12,slowline=26,period = 9): #預設slowline = EMA26 ,fastline = EMA12,DEA取9日
        ExpofPer = 2/(period+1)
        self.stPrice = self.DIFF(fastline,slowline).dropna()
        dea = self.ewmaCal(period, ExpofPer)
        return dea.dropna()


    def MACD(self,fastline=12,slowline=26,DEAperiiod=9):
        macd = self.DIFF(fastline,slowline) -self.DEA(fastline,slowline,DEAperiiod)
        return macd.dropna()

    def RSV(self,period =9):
        rsv = pd.Series([np.nan] * len(self.CLOSE), index=self.CLOSE.index)
        for i in range(period-1,len(self.CLOSE)):
            periodHigh = np.max(self.High[i-period+1:i+1])
            periodLow = np.min(self.LOW[i-period+1:i+1])
            rsv[i]= 100*(self.CLOSE[i]-periodLow)/(periodHigh - periodLow)
        return rsv.dropna()

    def Kvalue(self,weightK = 2/3,weightRSV =1/3,rsv_P=None): #前一日的Ｋ權重(預設2/3)+當日ＲＳＶ權重(預設1/3)
        rsv = rsv_P if type(rsv_P)== pd.core.series.Series else self.RSV()
        k = [50]
        for i in range(len(rsv)):
            k.append(weightK*k[-1] + weightRSV*rsv[i])
        kvalue = pd.Series(k[1:],index=rsv.index) #k[1:] 扣掉k的初始值
        return kvalue

    def Dvalue(self,weightD=2/3,weightK=1/3,kval_P=None): #前一日的D權重(預設2/3)+當日K權重(預設1/3)
        kvalue = kval_P if type(kval_P)== pd.core.series.Series else self.Kvalue()
        d=[50]
        for i in range(len(kvalue)):
            d.append(weightD*d[-1] + weightK*kvalue[i])
        dvalue = pd.Series(d[1:],index=kvalue.index) #d[1:] 扣掉d的初始值
        return dvalue
    
    def Jvalue(self,weightD =2 ,weightK=3,dval_P = None,kval_P=None): #當日的Ｋ權重(預設3)+當日Ｄ權重(預設2)
        dvalue = dval_P if type(dval_P)== pd.core.series.Series else self.Dvalue()
        kvalue = kval_P if type(kval_P)== pd.core.series.Series else self.Kvalue()
        jvalue = pd.Series(map(lambda x: x[0] * weightK - x[1] * weightD, zip(kvalue,dvalue)), index=dvalue.index)
        return jvalue

    def KDJvalue(self):
        rsv = self.RSV()
        kvalue=[50];dvalue=[50];jvalue=[]

        for i in range(0,len(rsv)):
            kvalue.append((2/3)*kvalue[-1] + (1/3)*rsv[i])
            dvalue.append((2/3)*dvalue[-1] + (1/3)*kvalue[-1])
            jvalue.append(3*kvalue[-1]-2*dvalue[-1])

        kdjvalue = pd.DataFrame({ "Kvalue" :kvalue[1:],"Dvalue":dvalue[1:],"Jvalue":jvalue},index=self.RSV().index)
        return kdjvalue

    def judge_paramater(self,base_p,ref_p):
        if base_p == None:
            return_p = ref_p
        else:
            return_p = base_p
        return return_p







