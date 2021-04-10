import ccxt
from datetime import datetime
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import calendar
import pandas as pd
import mplfinance as mpf
from mplfinance.original_flavor import candlestick_ohlc
import matplotlib.dates as mdates
import matplotlib


# collect the candlestick data from Binance
coinbase = ccxt.coinbasepro()
trading_pair = 'NU/USD'
now = datetime(2021, 3, 1)
unixtime = calendar.timegm(now.utctimetuple())
since = (unixtime - 60*60) * 1000 # UTC timestamp in milliseconds
candles = coinbase.fetch_ohlcv(trading_pair, '6h', since = since)


dates = []
open_data = []
high_data = []
low_data = []
close_data = []
ohlc = []



# format the data to match the charting library
for candle in candles:
    dates.append(datetime.fromtimestamp(candle[0] / 1000.0).strftime('%Y-%m-%d %H:%M:%S'))
    open_data.append(candle[1])
    high_data.append(candle[2])
    low_data.append(candle[3])
    close_data.append(candle[4])

#dates=mdates.date2num(dates.index) #creates a date column stored in number format (for OHCL bars)

df = pd.DataFrame({'dates':dates, 'open':open_data, 'high':high_data, 'low':low_data, 'close':close_data})

fig, ax1 = plt.subplots() #Create Plots
candlestick_ohlc(ax1, ohlc, width=.5, colorup='c', colordown='k', alpha=0.75)
#for i in open_data:
 #   append_me = open_data[i]
  #  ohlc.append(append_me)

# plot the candlesticks
def plot():
    fig = go.Figure(data=[go.Candlestick(x=dates,
                           open=open_data, high=high_data,
                           low=low_data, close=close_data)])
    fig.update_layout(
        )
    
    fig.show()
    return fig

#ax1.xaxis.set_major_locator(matplotlib.dates.MonthLocator())
ax1.xaxis.set_major_formatter(matplotlib.dates.DateFormatter('%m-%d'))
ax1.scatter(df['dates'], df['close'])

#fig = plot()

plt.show()
#print(df['dates'])
#print(df)
