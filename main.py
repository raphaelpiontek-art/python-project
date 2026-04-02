#%%%%%%%This file runs the programm in our console%%%%%%%%

#import our previously created functions
from datafetcher import * 
from portfolio.weigths import *

#import also our normal toolkit
from datetime import datetime
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import yfinance as yf
#we set variables for coloring the console outputs
RED = '\033[31m'
GREEN = '\033[32m'
RESET = '\033[0m'

#create the interface for the user
print("Welcome to Piontek & Poulard, your personal programm for creating portfolios. Start by selecting your financial product. We accept 15 producs at maximum")

#initialize the counter of products in our portfolio
i = 0
portfolio = []




#Iterations for the user selecting it's portfolio
while True:
    user_input = input(f"Ticker or ISIN of the whished product ({i} out of 15), exit with STOP: ")
    
    #If user typed STOP or we have the maximum of 15, we break
    if user_input == "STOP" or i == 15:
        print(f"{GREEN}You are finished with the product selection, we proceed now with the weigthing{RESET}")
        break
    
    #check if it's a TICKER or ISIN
    #we have to convert the ISIN into an TICKER, because we build everything for a Ticker
    if len(user_input) == 12 or len(user_input)== 13 : #ISIN are 12 long and often people forget with copy pasting to delete the " " so we also say 13
         
         
        if isin_converter(user_input) == None: 
            #function gives None if ISIN is not correct
             print(f"{RED}You inserted a wrong ISIN!{RESET}")
             continue
        else:
            #if it's correct, apply the TICKER to user_input
            user_input = isin_converter(user_input)
    
    #check if the TICKER is correct
    #fetch_market_caps return 0 if it didn't found the product
    if fetch_market_caps([user_input])[user_input] == 0 :
        print(f"{RED}Your input {user_input} was incorrect!!{RESET}")
    elif user_input in portfolio:
        print(f"{RED}Your input {user_input} is already in the portfolio!{RESET}")
    else:
        print(f"{GREEN} The product {user_input} was added to your portfolio{RESET}")
        i = i + 1
        portfolio.append(user_input)

#Choosing which optimisation strategy the user wants to choose
print("your corrent portfolio consists of the following")
print(portfolio)



#collect the dates in which the user wants to observe his portfolio, before creating the weighting we 
while True:
        
    #demand the dates that is going to be used in the function
    start = input("Which Start Date (Format: YYYY-MM-DD) do you want to choose : ")
    end = input("Which End Date (Format: YYYY-MM-DD) do you want to choose : ")
    
    # check if the date format is correct
    try:
        start_date = datetime.strptime(start, "%Y-%m-%d")
        end_date  = datetime.strptime(end, "%Y-%m-%d")
        
    except ValueError:
        print(f"{RED}Invalid date format, please use YYYY-MM-DD{RESET}")
        continue

    # check if end date is before start date, because we that would cause errors in our function
    if end < start:
        print(f"{RED}End date cannot be before start date{RESET}")
        continue   
    break   # if dates don't have errors break the loop

print("We personally curated 4 types of portfolios strategies for you. Please select your choosen strategy with the number given in the brackets")

#we do a loop, so the process repeats, even if the user input is wrong
while True:
    
    if len(portfolio)==1:
        #if there is only 1 product, we skip weigthing
        print("But weigting the portfolio with only 1 product, doesn't make sense so we skip the weighting part")
        break
       
    #asking the user 
    user_input = input("equal weight(1), market cap weighting(2), minimum variance(3) or maximum return(4): ") 

    #depending on the user input we run our function to calulate our weigths that are in portfolio -> weights.py
    if int(user_input) == 1:
        #equal weight case
        print(f"{GREEN}You selected the equal weighting option{RESET}")
        portfolio_weights = Equal_Weight(portfolio)
        break
    elif int(user_input) == 2:
        #market cap weighting case
        print(f"{GREEN}You selected the market cap weighting option{RESET}")
        portfolio_weights = market_cap_weight(portfolio)
        break
    elif int(user_input) == 3:
        #mminimum variance case
        print(f"{GREEN}You selected the minimum variance weighting option{RESET}")
        print("For these option we will use your select time frame when assesing the variance of your portfolio")
      
        portfolio_weights = minimum_variance(portfolio, start_date, end_date)
        break
    elif int(user_input) == 4:
        #maximum return case
        print(f"{GREEN}You selected the maximum return weighting option{RESET}")
        print("For these option we need to know which time window should be considered when assessing the variance of your portfolio and what the minimum weight is")
        
        #inner loop for demanding the min weight of each asset
        while True:
            print("The minimum weight should not be higher then the equal weights (not more then "+str(100/len(portfolio)) + "%) !")
            min_weight = input("What should be the minimum weight of each asset(Format is 0.XXXX), it can be 0 as well?: ")
            
            #check if the user complies with the required format
            if not(0 <= float(min_weight) <=100/len(portfolio)):
                print(f"{RED}Wrong Input of the minimum weight{RESET}.")
                continue
            break
        portfolio_weights = max_return_min_weight(portfolio, start_date, end_date, min_weight)
        break
    else:
        print(f"{RED} Wrong input, pls try again{RESET}")
        continue
        
        

print(f"{GREEN}Your portfolio weights are equal to: {portfolio_weights}{RESET}")


#calculate some key statistics

#the mean of the given portfolio
prices = fetch_prices(portfolio, start_date, end_date)
values = prices.values
returns = (values[1:] - values[:-1]) / values[:-1]
mean_returns = np.mean(returns, axis=0) * 252

print(f"Here are the mean retunrs {mean_returns} in order of your portfolio")
portfolio_return = np.dot(list(portfolio_weights.values()), mean_returns)
print(f"Expected annual portfolio return: {portfolio_return:.2%}")

#calculate the portfolio variance
cov_matrix   = np.cov(returns.T)  # covariance matrix
weights_array = np.array(list(portfolio_weights.values()))
variance     = weights_array @ cov_matrix @ weights_array * 252  # annualized
print(f"Portfolio Variance: {variance:.4f}")

#max drawdown calculation
portfolio_values = prices @ weights_array  # weighted portfolio value
rolling_max      = np.maximum.accumulate(portfolio_values)
drawdown         = (portfolio_values - rolling_max) / rolling_max
max_drawdown     = drawdown.min()
max_drawdown_date = drawdown.idxmin()
print(f"Max Drawdown: {max_drawdown:.2%} occurred in {max_drawdown_date.year}")

#sharp ratio
risk_free_rate = 0.02  # 2% annual risk free rate, adjust as needed
volatility     = np.sqrt(variance)
sharpe_ratio   = (portfolio_return - risk_free_rate) / volatility
print(f"Sharpe Ratio: {sharpe_ratio:.4f}")

#creating a plot with comparaison of your portfolio with a benchmark
#we choose to take the IShares MSCI World ETF
benchmark = fetch_prices(["URTH"],start_date, end_date)


# normalize both to 100 at start for comparison
portfolio_normalized = portfolio_values / portfolio_values.iloc[0] * 100
benchmark_normalized = benchmark / benchmark.iloc[0] * 100

#squeeze both our benchmark and portfolio_values to have it 1 dimensional so we can do a lineplot 
portfolio_normalized = portfolio_normalized.squeeze()
benchmark_normalized = benchmark_normalized.squeeze()

sns.lineplot(x=portfolio_values.index, y=portfolio_normalized, label="Portfolio")
sns.lineplot(x=benchmark.index, y=benchmark_normalized, label="IShares MSCI World ETF")

plt.title("Portfolio vs IShares MSCI World ETF")
plt.xlabel("Date")
plt.ylabel("Indexed Value (Base 100)")
plt.legend()
plt.show()
# restart the programm if the user wants to create another portfolio
while True:
    restart = input("Do you want to create another portfolio? (YES/NO): ")
    if restart == "YES":
        exec(open("main.py").read())
        break
    elif restart == "NO":
        print("Thank you for using Piontek & Poulard. Goodbye!")
        break
    else:
          print(f"{RED}Invalid input, please type yes or no{RESET}")
