#import libraries
import yfinance as yf
import datetime as dt
import pandas as pd
from pandas_datareader import data as pdr
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as mticker
import datetime as datetime
import numpy as np
import mplfinance as mpf
from mplfinance.original_flavor import candlestick_ohlc
import scipy
from scipy import stats

#yahoo finance pandas workaround
yf.pdr_override()

# pick your smas
smasUsed=[1,2,5,8,10]

#Sets start point and end point of dataframe
start =dt.datetime(2020,9,1)- dt.timedelta(days=max(smasUsed))
now = dt.datetime.now()

#Asks for stock ticker
stock = input("Enter the stock symbol : ")


#Runs loop until user enters 'quit'
while stock != "quit":

  prices = pdr.get_data_yahoo(stock, start, now) #which stock?

  fig, ax1 = plt.subplots() #Create Plots

#This for loop calculates the SMAs for the stated periods and appends to dataframe
  for x in smasUsed:
    sma=x
    prices['SMA_'+str(sma)] = prices.iloc[:,4].rolling(window=sma).mean() #calcaulates thing and creates column

  prices["Date"]=mdates.date2num(prices.index) #creates a date column stored in number format (for OHCL bars)


#choose moving average
  BBperiod=15
  stdev=2
  prices['SMA'+str(BBperiod)] = prices.iloc[:,4].rolling(window=BBperiod).mean() #calculates thing and creates a column in the dataframe
  prices['STDEV']=prices.iloc[:,4].rolling(window=BBperiod).std() #calculates standard deviation and creates col
  prices['LowerBand']=prices['SMA'+str(BBperiod)]-(stdev*prices['STDEV']) #calculates lower bollinger band
  prices['UpperBand']=prices['SMA'+str(BBperiod)]+(stdev*prices['STDEV']) #calculates upper band

#creates array for OHLC candle sticks
  ohlc = []

  for i in prices.index:
#append OHLC prices to make the candlestick
    append_me = prices["Date"][i], prices["Open"][i], prices["High"][i], prices["Low"][i], prices["Adj Close"][i], prices["Volume"][i]
    ohlc.append(append_me)

  lin_out = stats.linregress(prices['Date'], prices['High'])#calculates lineregress from high
  lin_out1 = stats.linregress(prices['Date'], prices['Low'])#calculates lineregress from low

  x_fit = np.linspace(np.min(prices['Date']), np.max(prices['Date']))#'fits x-axis from the beggining to end of dates
  y_fit = x_fit*lin_out[0]+ lin_out[1]# fits yaxis

  x_fit1 = np.linspace(np.min(prices['Date']), np.max(prices['Date']))
  y_fit1 = x_fit1*lin_out1[0]+ lin_out1[1]

  candlestick_ohlc(ax1, ohlc, width=.5, colorup='c', colordown='k', alpha=0.75)

  #Pivot Points
  pivots=[] #Stores pivot values
  dates=[]  #Stores Dates corresponding to those pivot values
  counter=0 #Will keep track of whether a certain value is a pivot
  lastPivot=0 #Will store the last Pivot value

  Range=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0] #Array used to iterate through stock prices
  dateRange=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0] #Array used to iterate through corresponding dates
  for i in prices.index: #Iterates through the price history
    currentMax=max(Range, default=0) #Determines the maximum value of the 10 item array, identifying a potential pivot
    value=round(prices["High"][i],2) #Receives next high value from the dataframe

    Range=Range[1:9] # Cuts Range array to only the most recent 9 values
    Range.append(value) #Adds newest high value to the array
    dateRange=dateRange[1:9]  #Cuts Date array to only the most recent 9 values
    dateRange.append(i) #Adds newest date to the array

    if currentMax == max(Range, default=0): #If statement that checks is the max stays the same
      counter+=1 #if yes add 1 to counter
    else:
      counter=0 #Otherwise new potential pivot so reset the counter
    if counter==5: # checks if we have identified a pivot
      lastPivot=currentMax #assigns last pivot to the current max value
      dateloc=Range.index(lastPivot) #finds index of the Range array that is that pivot value
      lastDate=dateRange[dateloc] #Gets date corresponding to that index
      pivots.append(currentMax) #Adds pivot to pivot array
      dates.append(lastDate) #Adds pivot date to date array
  print()

  pivot_high_1 = prices['High'][-100:-1].max()
  pivot_high_2 = prices['High'][-200:-1].max()

  pivot_low_1 = prices['Low'][-100:-1].max()
  pivot_low_2 = prices['Low'][-200:-1].max()

  A = [prices['High'][-100:-1].idxmax(), pivot_high_1]
  B = [prices['High'][-200:-1].idxmax(), pivot_high_2]

  A1 = [prices['Low'][-100:-1].idxmax(), pivot_low_1]
  B1 = [prices['Low'][-200:-1].idxmax(), pivot_low_2]

  x1_high_values = [A[0], B[0]]
  y1_high_values = [A[1], B[1]]

  x1_low_values = [A1[0], B1[0]]
  y1_low_values = [A1[1], B1[1]]

  timeD=dt.timedelta(days=120) #Sets length of dotted line on chart

  rolling_std = (prices['Close'] - prices['High']).rolling(20).std()

  for index in range(len(pivots)) : #Iterates through pivot array

    #print(str(pivots[index])+": "+str(dates[index])) #Prints Pivot, Date couple
    plt.plot_date([dates[index]-(timeD*.075), dates[index]+timeD], #Plots horizontal line at pivot value
                [pivots[index], pivots[index]], linestyle="--", linewidth=1, marker=',')
    plt.annotate(str(pivots[index]), (mdates.date2num(dates[index]), pivots[index]), xytext=(-10, 7),
            textcoords='offset points',fontsize=7, arrowprops=dict(arrowstyle='-|>'))

  ax1.plot(x_fit, y_fit, linewidth = 4, color = 'k', alpha = 0.2)
  ax1.plot(x_fit1, y_fit1, linewidth = 4, color = 'k', alpha = 0.2)

  prices['UpperBand'].plot(label='close',color='lightgray')
  prices['LowerBand'].plot(label='close', color='lightgray')
  plt.xlabel('Date') #set x axis label
  plt.ylabel('Price') #set y axis label
  plt.title(stock+" - Daily") #set title
  plt.ylim(prices["Low"].min(), prices["High"].max()*1.05) #add margins
  #plt.yscale("log")

  ax1.axhline(y = (pivot_high_1), color = 'r')
  ax1.axhline(y = pivot_high_2, color = 'g')
  ax1.axhline(y = pivot_low_1, color = 'r')
  ax1.axhline(y = pivot_low_2, color = 'g')
  ax1.plot(rolling_std, color = 'k', linestyle = ':')

  plt.show()
  # print()
  stock = input("Enter the stock symbol : ") #Asks for new stock
