# encoding: utf-8
#!/usr/bin/python3
import tushare as ts
import pymysql
import time
import sys



# Open database connection
db = pymysql.connect(host='127.0.0.1',
                     port=6001,
                     user='dump',
                     password='111',
                     database='pe')
 
# Create a cursor object 
cursor = db.cursor()

# Set Tushare data source 
ts.set_token('YOUR_TUSHARE_API_TOKEN')
pro = ts.pro_api()


# Find the lowest PB and PE value
cursor.execute('select ts_code,min(pe),min(pb) from pe_test where pe>0 and pb>0 group by ts_code order by ts_code')

# Fetch the result as python object
value = cursor.fetchall() 



df = pro.daily_basic(**{
    "ts_code": "",
    "trade_date": sys.argv[1],
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
df = df.fillna(0.0)


for i in range(0,len(value)):
    ts_code = value[i][0]
    min_pe = value[i][1]
    min_pb = value[i][2]

    for j in range(0, len(df.ts_code)):
        if ts_code == df.ts_code[j] and df.pe[j] < min_pe and df.pe[j]>0:
            print("ts_code: "+ts_code)
            print("history lowest PE : "+ str(min_pe))
            print("current PE found: "+ str(df.pe[j]))
        if ts_code == df.ts_code[j] and df.pb[j] < min_pb and df.pb[j]>0:
            print("ts_code: "+ts_code)
            print("history lowest PB : "+ str(min_pe))
            print("current PB found: "+ str(df.pe[j]))


cursor.close()
db.close()
