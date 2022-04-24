# MatrixOne Stock Analysis Python Application

This is a python application example with MatrixOne. Checkout this [tutorial](https://github.com/matrixorigin/matrixone/blob/main/docs/en/MatrixOne/Develop/develop_python_application.md) about how to start to build it from ground up. 


## Usage

1. Initialization 

Install required modules. 

```bash
pip3 install -r requirements.txt
```

2. Load historical data. 
```bash 
# Execute under the matrixone_python_app directory
python -m stock_analysis.main fetchData --tushareToken='YOUR_TUSHARE_API_TOKEN'
```

3. Find lowest P/E stock.

```bash

# Find the lowest P/E after market close on 22nd, April 2022
python3 -m stock_analysis.main findLowPE --tushareToken='YOUR_TUSHARE_API_TOKEN' --tradeDate='20220422'

# Find the lowest P/E on the day if you don't specify tradeDate
python3 -m stock_analysis.main findLowPE --tushareToken='YOUR_TUSHARE_API_TOKEN' 
```

4. Find lowest P/B stock.

```bash

# Find the lowest P/B after market close on 22nd, April 2022
python3 -m stock_analysis.main findLowPB --tushareToken='YOUR_TUSHARE_API_TOKEN' --tradeDate='20220422'

# Find the lowest P/E on the day if you don't specify tradeDate
python3 -m stock_analysis.main findLowPB --tushareToken='YOUR_TUSHARE_API_TOKEN' 

```

5. Update your dataset. 

```bash

# Update your selected stock data until the most recent
python -m stock_analysis.main fetchData --tushareToken='YOUR_TUSHARE_API_TOKEN' --stockCodes='000001.SZ,600000.SH'


# Update all stock data between a time range
python -m stock_analysis.main fetchData --tushareToken='YOUR_TUSHARE_API_TOKEN' --startDate=20220424 —endDate=20220424
```