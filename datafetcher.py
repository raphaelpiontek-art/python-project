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
            for item in data[0]["data"]:
                if item.get("exchCode") == "UW":
                     return item["ticker"]
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
    prices.dropna(how="any", inplace=True)

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

