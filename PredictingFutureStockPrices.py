# step 1
# import libraries
import math
import matplotlib.pyplot as plt
import numpy as np
from pandas_datareader import data

# pull amazon's data from 5 years ago
amazon = data.DataReader('AMZN', 'yahoo', start='1/1/2014')
amazon.head()

# step 2
# calculate number of days that have elapsed in our chosen time window
time_elapsed = (amazon.index[-1] - amazon.index[0]).days

# step 3
# calculate compounded annualized growth rate over the length of the dataset + standard deviation
total_growth = (amazon['Adj Close'][-1] / amazon['Adj Close'][1])

# annualize this percentage
# first, convert to number of years elapsed
years_elapsed = time_elapsed / 365.0 
# then, raise the total growth to the inverse of the number of years
cagr = total_growth**(1/years_elapsed) - 1

# calculate standard deviation of daily price changes
std_dev = amazon['Adj Close'].pct_change().std()

# because there are roughy ~252 trading days in a year, scale it by an annualization factor
number_of_trading_days = 252
std_dev = std_dev*math.sqrt(number_of_trading_days)

# now we have our inputs needed to run the simulation
print ("cagr (mean returns): ", str(round(cagr,4)))
print ("std_dev (standard deviation of return): ", str(round(std_dev,4)))

# step 4 
# generate random values for 252 days (1 trading year)
daily_return_percentages = np.random.normal(cagr/number_of_trading_days, std_dev/math.sqrt(number_of_trading_days),

number_of_trading_days) + 1

# create "random walk" distribution
price_series = [amazon['Adj Close'][-1]]

for j in daily_return_percentages:
    price_series.append(price_series[-1] * j)

# plot above data        
plt.plot(price_series)
plt.show()

# simulate over larger sample size
number_of_trials = 3000

# create another array for closing prices on last trading day
closing_prices = []

# iterate throught the number of trials
for i in range(number_of_trials):
    # calculate randomized return percentages 
    # using mean / std dev value above
    daily_return_percentages = np.random.normal(cagr/number_of_trading_days, std_dev/math.sqrt(number_of_trading_days),
number_of_trading_days)+1
    price_series = [amazon['Adj Close'][-1]]

    for j in daily_return_percentages:
        # extrapolate price out for next year
        price_series.append(price_series[-1] * j)
    
    # append closing prices in last day of window for histogram
    closing_prices.append(price_series[-1])
  
    # plot all random walks
    plt.plot(price_series)
    


plt.show()

#plot histogram
plt.hist(closing_prices,bins=40)

plt.show()

# we can check mean of all ending prices --> determine most probable ending point
mean_end_price = round(np.mean(closing_prices),2)
print("Expected price: ", str(mean_end_price))

# split distribution into percentiles to see relationship b/w risk and reward

# top 10% of possible outcomes
top_ten = np.percentile(closing_prices,100-10)

# bottom 10% of possible outcomes
bottom_ten = np.percentile(closing_prices,10);

#create histogram again
plt.hist(closing_prices,bins=40)
#append w/ top 10% line
plt.axvline(top_ten,color='r', linestyle = 'dashed', linewidth = 2)
#append w/ bottom 10% line
plt.axvline(bottom_ten,color='r',linestyle = 'dashed', linewidth = 2)
#append with current price
plt.axhline(amazon['Adj Close'][-1],color='g', linestyle = 'dashed', linewidth = 2)

plt.show() 
