import datetime
import twstock
import pandas as pd

from bs4 import BeautifulSoup as bs
#from datetime import timedelta ,datetime
import requests


class StockCrawler(twstock.Stock):
    today = datetime.datetime.today()
    def __init__(self, sid: str, initial_fetch: bool = True):
        super().__init__(sid, initial_fetch)
        global today


    def AppendStockdf(self):

        stock = self.fetch_from(2013,1)
        stockdf = pd.DataFrame(stock)
        stockdf.to_csv('./stocklist/'+str(self.sid)+'_stockinfo.csv')
        return ("Fetche_Done")

    def UpdateTotheLast(self):
        stockdf = self.readfiletodataframe()

        today = datetime.date.today()
        strdate = stockdf.index[-1]
        data_last = self.strtodate(strdate)  # 資料庫資料最後的時間
        lastdays = (today - data_last).days  # lastdays  >0 代表資料沒有更新到最新日期

        if 0 < lastdays < 32:
            # update_d = self.fetch_31()
            # update_d = pd.DataFrame(update_d).set_index("date")
            update_d = self.formatdata(self.fetch_31())
            stockdf = self.data_merge(stockdf, update_d)

        elif lastdays > 31:
            # update_d = self.fetch_from(data_last.year, data_last.month)  # data_last 資料裡最後的更新時間
            # update_d = pd.DataFrame(update_d).set_index("date")
            update_d = self.formatdata(self.fetch_from(data_last.year, data_last.month))
            stockdf = self.data_merge(stockdf, update_d)
        else:
            pass
        # stockdf.to_csv('./stocklist/'+str(self.sid)+'_stockinfo.csv',index="date")

        return stockdf


    def readfiletodataframe(self):
        stockdf = pd.DataFrame
        try:
            stockdf = pd.read_csv('./stocklist/'+str(self.sid)+'_stockinfo.csv', index_col="date")
        except FileNotFoundError:
            print("找不到", str(self.sid), "名稱或讀取文件失敗")
        else:
            pass

        return stockdf

    @classmethod
    def data_merge(cls, df1: pd.DataFrame, df2: pd.DataFrame):
        new_data= df1.append(df2).drop_duplicates()  # drop_duplicates()去掉重複行
        return new_data



    def strtodate(self, str_date: str):  # str_date參考形式為2019-01-20
        year, month, day = map(int,str_date.split('-'))
        date = datetime.date(year,month,day)
        return date

    def formatdata(self,orignal_data):
        new_df = pd.DataFrame(orignal_data)
        indexlist = list(new_df["date"])
        for i ,e in enumerate(new_df["date"]):
            print(str(e),e)
            indexlist[i] = str(e).split(" ")[0]
        new_df["date"] = indexlist
        return new_df


"""
Created on Wed Feb 27 18:47:31 2019
針對元大網頁抓取證券商對個股的交易資料並整理

@author: ray
"""



class stockdealers():
    
    def __init__(self):
        pass

    def crawl_webdata(self,stockcode,select_date):
        soup = self._tryurl(stockcode,select_date)
        dealer_dic = {}
        d_dic = {}
        timedate = soup.select("script[language]")[12].text.splitlines()[2].split("=")[-1][:-1]
        dealer_dic[timedate[2:-1]]={}
        for content in soup.select('tr > td.t0 ')[0].findAll("tr",attrs = {"id":None}):
            if content.td["class"][0] in ['t4t1',"t3n1"]:

                dealers = content.text.splitlines()[1:]
                dealer_dic[timedate[2:-1]].update( self._convertdatatodict(dealers[:5],timedate,d_dic))
                dealer_dic[timedate[2:-1]].update( self._convertdatatodict(dealers[5:],timedate,d_dic))
                
        return dealer_dic
    
    def crawl_by_dates(self,code,date_start,date_end):
        date_start = datetime.datetime.strptime(date_start,'%Y-%m-%d').date()
        date_end   = datetime.datetime.strptime(date_end,'%Y-%m-%d').date()
        d_dic = {}
        for n in range(int ((date_end - date_start).days)+1):
            day = date_start + datetime.timedelta(n)
            str_day = str(day).replace('-','/')
            if day.isoweekday() in [1,2,3,4,5,6]:   #2018-12-22前twse星期六也有機會開盤
                 info_value = self.crawl_webdata(code,str(day))
                 if info_value[str_day] != {} :
                     d_dic.update(info_value)
                 else : pass
            else : pass
        
        return d_dic
        
    
    
    @staticmethod
    def search_dealerinfo(dealer_dic,specific_dealername):
        # dealer_dic ＝{date:{證券商：{'買進張數': .., '賣出張數': .., '總成交量': .., '占當日成交比重':.. , '日期':... }}
        dealer_n = {}
        for day in dealer_dic:
            for name in dealer_dic[day]:
                if specific_dealername in name and name not in dealer_n:
                    dealer_n[name]={day:dealer_dic[day][name]}
                elif name in dealer_n:
                    dealer_n[name].update({day:dealer_dic[day][name]})
                else :pass
        return dealer_n
    
                    
    @staticmethod
    def _convertdatatodict(datalist,timedate,d_dic):
        if '\xa0' in datalist:
            pass
            
        else:
            datalist[1:4] = map(lambda x:int(x.replace(',','')),datalist[1:4]) #處理分號與轉換int
            #[買賣超券商,買進張數,賣出張數,買賣超,佔成交比重]
            d_dic[datalist[0]]={"買進張數": datalist[1],
                                "賣出張數":datalist[2]*(-1),
                                "總成交量":datalist[1]+datalist[2]*(-1),
                                "占當日成交比重":float(datalist[4].split("%")[0])/100,
                                "日期":timedate[2:-1] }
        return d_dic
    
    @staticmethod
    def _tryurl(code,datadate):
        #date 形式 2016-12-20
        url = 'https://jdata.yuanta.com.tw/z/zc/zco/zco.djhtm?a='+str(code)+'&e='+str(datadate)+'&f='+str(datadate)
        try:
            page = requests.get(url)
        except requests.exceptions.RequestException as error:
            print(error)
        soup = bs(page.text,"lxml")
        
        return soup
    










