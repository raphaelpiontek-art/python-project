#datafetcher connection to yfinance
# import of packages
import yfinance as yf
import pandas as pd
import requests

#converting ISIN's to tickers using requests to the OpenFIGI API
def isin_converter(isin: str ) -> str:
    # starting the conversion process by sending a POST request to the OpenFIGI API with the ISIN as the identifier
    url     = "https://api.openfigi.com/v3/mapping"
    headers = {"Content-Type": "application/json"}
    payload = [{"idType": "ID_ISIN", "idValue": isin}]
    
    try: 
        response = requests.post(url, json=payload, headers=headers)
        data = response.json()

        if data and "data" in data[0] and len(data[0]["data"]) > 0:
            return data[0]["data"][0]["ticker"]
        else:
            return None
    except Exception as e:
        print(f"Error converting ISIN {isin}: {e}")
        return None

def convert_isins_to_tickers(isins: list) -> list:
    # isins: List of ISINs to be converted
    # returns List of corresponding tickers, None for ISINs that could not be converted.
    tickers = []
    for isin in isins:
        ticker = isin_converter(isin)
        tickers.append(ticker)
    return tickers


#fetching historical prices for gicen tickers and time period
def fetch_prices(tickers: list, start_date: str, end_date: str) -> pd.DataFrame:
    # tickers: List of tickers 
    # start_date: Start date for historical data in YYYY-MM-DD
    # end_date: End date for historical data 
    #returns DataFrame with dates as index and tickers as columns.

    # auto_adjust=True uses split/dividend adjusted prices
    data = yf.download(tickers, start=start_date, end=end_date, auto_adjust=True, progress=False)
    prices = data["Close"]
    # drop rows where all prices are NaN, then fill remaining NaN values using forward fill and backward fill
    prices.dropna(how="all", inplace=True)

    prices.ffill(inplace=True)

    prices.bfill(inplace=True)
    


    return prices

def fetch_market_caps(tickers: list) -> dict:
    # tickers: List of tickers 
    # returns Dictionary with tickers as keys and market caps as values.
    caps = {}
    for ticker in tickers:
        info = yf.Ticker(ticker).info #fetching Market Cap for each ticker, 0 if not available
        caps[ticker] = info.get("marketCap", 0)
    return caps
def fetch_benchmark(start: str, end: str) -> pd.Series:
    # fetches an MSCI World proxy ETF as Benchmark
    data = yf.download("URTH", start=start, end=end, auto_adjust=True, progress=False)
    return data["Close"].squeeze()
    # squeeze() converts the DataFrame to a Series if it has only one column, which is the case for the benchmark.

# function to covnert prices into Euros
def convert_prices_to_Euro(prices: pd.DataFrame, tickers: list, start_date: str, end_date: str) -> pd.DataFrame:
    # copy the original prices
    prices_euro = prices.copy()

    for ticker in tickers:
        # fetch the currency for the ticker
        currency = yf.Ticker(ticker).info.get("currency", "USD")  # Set currency to usd if not available
        if currency == "EUR":
            continue  
        
        # Set the exchange rate ticker based on the currency
        fx_ticker = f"{currency}EUR=X"

        # Fetch the exchange rate data for the specified period
        fx_data = yf.download(fx_ticker, start=start_date, end=end_date, auto_adjust=True, progress=False) 
        fx_rate = fx_data["Close"]
        if isinstance(fx_rate, pd.DataFrame):
            fx_rate = fx_rate.iloc[:,0] # if multiple columns, take the first one
        else:
            fx_rate = fx_rate.squeeze() # if its a DataFrame with one column, convert to Series

        # reindex the exchange rate to match the prices DataFrame , ffill fills missing values using forward fill method
        fx_rate = fx_rate.reindex(prices.index).ffill().bfill()

        # multiply the original prices by the exchange rate to convert to Euros
        prices_euro[ticker] = prices_euro[ticker] * fx_rate
    return prices_euro



