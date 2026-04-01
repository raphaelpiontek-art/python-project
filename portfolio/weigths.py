import numpy as np
import pandas as pd
from scipy.optimize import minimize
from datafetcher import *


#1 Equal Weighting
def Equal_Weight(tickers: list) -> dict:
    n = len(tickers)
    weight = 1/n
    return {ticker: weight for ticker in tickers}

#2 Market Cap Weighting
def market_cap_weight(tickers: list) -> dict:
    # Each Assets weight is proportional to its market cap relative to the total market cap of all assets in the portfolio.
    market_caps = fetch_market_caps(tickers)
    # Sum of all market caps
    total = sum(market_caps[ticker] for ticker in tickers)
    # Calculate weights
    return {ticker: market_caps[ticker] / total for ticker in tickers}

#3 Minimum Variance Portfolio using scipy optimization
def minimum_variance(tickers: list, start_date: str, end_date: str) -> dict:
    
    #calculate the prices using our function
    prices = fetch_prices(tickers, start_date, end_date)
    # Extract tickers from the DataFrame columns
    tickers = list(prices.columns)
    
    #Compute daily linear returns
    values  = prices.values
    returns = (values[1:] - values[:-1]) / values[:-1]
    
    #variance covariance matrix
    #mean return per asset
    mean_returns = returns.sum(axis=0) / len (returns)
    
    # centred returns
    centred_returns = returns - mean_returns
    
    #matrix
    T = len(returns)
    cov_matrix = (centred_returns.T @ centred_returns) / (T - 1)
    cov_matrix_annual = cov_matrix * 252 #annualization

    def portfolio_variance(w):
        return w @ cov_matrix_annual @ w
    
    # constraints and bounds:
    n = len(tickers)
    constraints = {"type": "eq", "fun": lambda w: np.sum(w) - 1} #weights must sum to 1
    bounds      = [(0.0, 1.0)] * n  # short selling is not allowed
    w0          = np.ones(n) / n  # we start using equal weights as initial guess
    # optimization using scipy
    result = minimize(portfolio_variance, w0, method="SLSQP", constraints=constraints, bounds=bounds)
    # return the optimal weights as a dictionary
    return {ticker: weight for ticker, weight in zip(tickers, result.x)}

    
#4 Maximum Return with Minimum Weight Constraint
def max_return_min_weight(tickers: list, start_date: str, end_date: str, min_weight: float) -> dict:
    
    #calculate the prices using our function
    prices = fetch_prices(tickers, start_date, end_date)

    tickers = list(prices.columns)
    values  = prices.values
    returns = (values[1:] - values[:-1]) / values[:-1]
    n = len(tickers)
    
    #annualised returns
    mean_returns = np.mean(returns, axis=0) * 252

    # minimize negative return to maximize return
    def negative_return(w, mr=mean_returns):
        return -w @ mr
    
    # constraints and bounds:
    constraints = {"type": "eq", "fun": lambda w: np.sum(w) - 1}  # weights sum to 1
    bounds      = [(min_weight, 1.0)] * n # minimum weight constraint
    w0          = np.ones(n) / n 
    
    # optimization using scipy
    result = minimize(negative_return, w0, method="SLSQP", bounds=bounds, constraints=constraints)
    
    return {ticker: weight for ticker, weight in zip(tickers, result.x)}
    
    
    

    










    
    
    




