import datetime
import twstock
import pandas as pd


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

    # def UpdatetheStartpoint(self, start_year=2013, start_month=1):  # 預設資料抓取起始點為20130101;
    #     stockdf = self.readfiletodataframe()
    #
    #     data_head = self.strtodate(stockdf.index[0])  # 資料庫資料最起始的時間
    #     startdays = (datetime.date(start_year, start_month, 1) - data_head).days
    #     # startdays >0 代表設定的資料時間早於資料目前最早時間
    #
    #     if startdays > 0:
    #         update_d = self.fetch_from(start_year, start_month, data_head.year, data_head.month)
    #         update_d = pd.DataFrame(update_d).set_index("date")
    #         stockdf = self.data_merge(update_d, stockdf)
    #     else:
    #         pass
    #
    #     return stockdf

    # def fetch_from(self, year_start: int, month_start: int, year_end = today.year, month_end = today.month):
    #     """Fetch data from year, month to what you want year month data"""
    #     # 改寫twstock方法 增加可設定的截止時間
    #     self.raw_data = []
    #     self.data = []
    #     for year, month in self._month_year_iter(month_start, year_start, month_end, year_end):
    #         self.raw_data.append(self.fetcher.fetch(year, month, self.sid))
    #         self.data.extend(self.raw_data[-1]['data'])
    #     return self.data


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


