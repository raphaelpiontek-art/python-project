#This envrionment was created to test all the function we want for our main.py but without having to always insert all the variable values
#like ticker, weights or Date

#our testing was deleted, but this can still be used to test specific functions or calculations



from datafetcher import * 
from portfolio.weigths import *
from datetime import datetime
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import yfinance as yf

portfolio = ["AAPL","MSFT","NVDA"]
portfolio_weights = {'AAPL': np.float64(0.3333333333333333), 'MSFT': np.float64(0.3333333333333333), 'NVDA': np.float64(0.3333333333333333)}
start_date = datetime.strptime("2004-01-01", "%Y-%m-%d")
end_date  = datetime.strptime("2026-01-01", "%Y-%m-%d")



