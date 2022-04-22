import logging
import time
import datetime
from stock_analysis.cli.modb_cli import MOClient
from stock_analysis.cli.tushare_cli import TuShareClient
import fire

logging.getLogger().setLevel(logging.INFO)


class StockAnalysis(object):

    def __init__(self, tushareToken,
                 dbPassword='111',
                 dbHost='127.0.0.1',
                 dbPort=6001,
                 dbName='stock',
                 dbUser='dump',
                 startDate="",
                 endDate="",
                 tradeDate=datetime.date.today().strftime('%Y%m%d'),
                 stockCodes=""):
        self.tushareToken = tushareToken
        self.dbPassword = dbPassword
        self.dbHost = dbHost
        self.dbPort = dbPort
        self.dbName = dbName
        self.dbUser = dbUser
        self.startDate = startDate
        self.endDate = endDate
        self.tradeDate = tradeDate
        self.stockList = [] if len(stockCodes) == 0 else stockCodes.split(",")

    """
    Fetch stock data within the specified date range [start_date, end_date] from tushare api.
    Args:
        start_date: start date for the requested stock data, YYYYMMDD, default is "", which means no limit.
        end_date: end date for the requested stock data, YYYYMMDD, default is "", which means no limit.
    """
    def fetchData(self):
        with TuShareClient(self.tushareToken) as tsCli:
            if len(self.stockList) == 0:
                pool = tsCli.apiCli.stock_basic(exchange='',
                                                list_status='L',
                                                adj='qfq',
                                                fields='ts_code,symbol,name,area,industry,fullname,list_date, market,exchange,is_hs')
                self.stockList = pool.ts_code

            logging.getLogger().info("Get stock number: %d", len(self.stockList))

            with MOClient(self.dbHost, self.dbUser, self.dbPassword, self.dbName, self.dbPort) as moCli:
                try:
                    # Create PE table if not exists
                    moCli.db_cursor.execute(
                        'create table if not exists pe(ts_code varchar(255), trade_date varchar(255), pe float, pb float)')
                    j = 1
                    for i in self.stockList:
                        logging.getLogger().info('Getting %d stock，Stock Code %s.', j, i)
                        # The interface is limited to be queried 200 times/minute, some little delays are necessary
                        time.sleep(0.301)
                        j += 1
                        try:
                            df = tsCli.apiCli.daily_basic(**{
                                "ts_code": i,
                                "trade_date": "",
                                "start_date": self.startDate,
                                "end_date": self.endDate,
                                "limit": "",
                                "offset": ""
                            }, fields=[
                                "ts_code",
                                "trade_date",
                                "pe",
                                "pb"
                            ])
                            if not df.empty:
                                df = df.fillna(0.0)
                                val_to_insert = df.values.tolist()
                                moCli.db_cursor.executemany(
                                    " insert into pe (ts_code, trade_date,pe,pb) values (%s, %s,%s,%s)",
                                    val_to_insert)
                        except Exception as e:
                            logging.getLogger().error('[%s]error occurred in loading, %s', i, e)

                except ConnectionError as e:
                    logging.getLogger().error("DB Error, %s", str(e))

    """
    Find stocks that the current P/E or P/B is even lower than the historical lowest
    """
    def findLowPE(self):
        with MOClient(self.dbHost, self.dbUser, self.dbPassword, self.dbName, self.dbPort) as moCli:
            try:
                moCli.db_cursor.execute(
                    'select ts_code,min(pe),min(pb) from pe where pe>0 and pb>0 group by ts_code order by ts_code')
                # Fetch the result as python object
                value = moCli.db_cursor.fetchall()
                with TuShareClient(self.tushareToken) as tsCli:
                    df = tsCli.apiCli.daily_basic(**{
                        "ts_code": "",
                        "trade_date": self.tradeDate,
                        "start_date": "",
                        "end_date": "",
                        "limit": "",
                        "offset": ""
                    }, fields=[
                        "ts_code",
                        "pe",
                        "pb"
                    ])
                    df = df.fillna(0.0)

                    for i in range(0, len(value)):
                        ts_code, min_pe, min_pb = value[i]

                        for j in range(0, len(df.ts_code)):
                            if ts_code == df.ts_code[j] and min_pe > df.pe[j] > 0:
                                print(df[j])
                                logging.getLogger().info("ts_code: %s", ts_code)
                                logging.getLogger().info("history lowest PE : %f", min_pe)
                                logging.getLogger().info("current PE found: %f", df.pe[j])
                            if ts_code == df.ts_code[j] and min_pb > df.pb[j] > 0:
                                print(df.pb[j])
                                logging.getLogger().info("ts_code: %s", ts_code)
                                logging.getLogger().info("history lowest PB: %f", min_pb)
                                logging.getLogger().info("current PB found: %f", df.pb[j])
            except Exception as e:
                logging.getLogger().error("fetch failed, %s", str(e))


if __name__ == '__main__':
    fire.Fire(StockAnalysis)
