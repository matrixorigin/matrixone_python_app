# encoding: utf-8
#!/usr/bin/python3
import tushare as ts
import pymysql
import time

# Open database connection
db = pymysql.connect(host='127.0.0.1',
                     port=6001,
                     user='dump',
                     password='111',
                     database='stock')
 
# Create a cursor object 
cursor = db.cursor()

# Create PE table
cursor.execute('drop table if exists pe')
cursor.execute('create table pe(ts_code varchar(255), trade_date varchar(255), pe float, pb float)') 


# Set Tushare data source 
ts.set_token('YOUR_TUSHARE_API_TOKEN')
pro = ts.pro_api()



pool = pro.stock_basic(exchange = '',
                        list_status = 'L',
                        adj = 'qfq',
                        fields = 'ts_code,symbol,name,area,industry,fullname,list_date, market,exchange,is_hs')

print('Get stock number：', len(pool)-1)

j = 1
for i in pool.ts_code:
    print('Getting %d stock，Stock Code %s.' % (j, i))
    
    #The interface is limited to be queried 200 times/minute, some little delays are necessary
    time.sleep(0.301)
    j+=1

    df = pro.daily_basic(**{
    "ts_code": i,
    "trade_date": "",
    "start_date": "",
    "end_date": "",
    "limit": "",
    "offset": ""
    }, fields=[
    "ts_code",
    "trade_date",
    "pe",
    "pb"
    ])


    if df.empty == False:
        df = df.fillna(0.0)
        val_to_insert = df.values.tolist()
        cursor.executemany(" insert into pe_test (ts_code, trade_date,pe,pb) values (%s, %s,%s,%s)", val_to_insert)
        

cursor.close()
db.close()