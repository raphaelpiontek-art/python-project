#datafetcher connection to yfinance
# import of packages
import yfinance as yf
import pandas as pd
#fetching historical prices for gicen tickers and time period
def fetch_prices(tickers:=list, start_date:=str, end_date:= str) -> pd.DataFrame:
    # tickers: List of tickers 
    # start_date: Start date for historical data in YYYY-MM-DD
    # end_date: End date for historical data 
    #returns DataFrame with dates as index and tickers as columns.

    # auto_adjust=True uses split/dividend adjusted prices
    data = yf.download(tickers, start=start_date, end=end_date, auto_adjust=True, progress=False)
    prices = data["Close"]
    prices.dropna(how="all", inplace=True)

    return prices
