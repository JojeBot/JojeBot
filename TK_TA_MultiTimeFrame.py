from tkinter import *
from tkinter import ttk

import numpy as np
import pandas as pd
from pandas_datareader import data as pdr

from scipy.stats import norm

import matplotlib.pyplot as plt
from yahoofinancials import YahooFinancials

from yahoo_fin import stock_info as si

from decimal import Decimal
from datetime import timedelta
from dateutil.relativedelta import relativedelta

import datetime as dt
import datetime as datetime
import yfinance as yf
import mplfinance as mpf




import math


class Searchpages:

    def __init__(self, master):
        master.title('Searchpage')
        self.entry_stock = ttk.Entry(width=30, font=('Arial', 15))
        self.entry_stock.grid(row=4, column=0, padx=15, columnspan=2)

        ttk.Button(text='1min', command=self.onemin).grid(row=6, column=0, padx=5)
        ttk.Button(text='5min', command=self.fivemin).grid(row=6, column=1)
        ttk.Button(text='15min', command=self.fifteenmin).grid(row=6, column=2)
        ttk.Button(text='1hour', command=self.hour).grid(row=6, column=3)
        ttk.Button(text='1day', command=self.day).grid(row=6, column=4)
        ttk.Button(text='Clear', command=self.clear).grid(row=6, column=5, padx=5)

    def onemin(self):
        ticker = [self.entry_stock.get()]

        prices = yf.download(tickers= ticker, start=datetime.datetime.now()-relativedelta(days=7), end=datetime.datetime.now(), interval="1m")

        mpf.plot(prices, type = 'candle', mav = (10, 30, 100), style = "nightclouds")
        #plt.plot(prices["Open"], label = prices)
        plt.show()

        self.clear()

    def fivemin(self):
        ticker = [self.entry_stock.get()]

        prices = yf.download(tickers= ticker, start=datetime.datetime.now()-relativedelta(days=7), end=datetime.datetime.now(), interval="5m")

        mpf.plot(prices, type = 'candle', mav = (10, 30, 100), style = "nightclouds")
        #plt.plot(prices["Open"], label = prices)
        plt.show()

        self.clear()

    def fifteenmin(self):
        ticker = [self.entry_stock.get()]

        prices = yf.download(tickers= ticker, start=datetime.datetime.now()-relativedelta(days=30), end=datetime.datetime.now(), interval="15m")

        mpf.plot(prices, type = 'candle', mav = (10, 30, 100), style = "nightclouds")
        #plt.plot(prices["Open"], label = prices)
        plt.show()

        self.clear()

    def hour(self):
        ticker = [self.entry_stock.get()]

        prices = yf.download(tickers= ticker, start=datetime.datetime.now()-relativedelta(days=60), end=datetime.datetime.now(), interval="1h")

        mpf.plot(prices, type = 'candle', mav = (10, 30, 100), style = "nightclouds")
        #plt.plot(prices["Open"], label = prices)
        plt.show()

        self.clear()

    def day(self):
        ticker = [self.entry_stock.get()]

        prices = yf.download(tickers= ticker, start="2022-1-1", end=datetime.datetime.now(), interval="1d")

        mpf.plot(prices, type = 'candle', mav = (10, 30, 100), style = "nightclouds")
        #plt.plot(prices["Open"], label = prices)
        plt.show()

        self.clear()

    def clear(self):
        self.entry_stock.delete(0, 'end')


def main():
    root = Tk()
    searchpage = Searchpages(root)
    root.mainloop()



if __name__ == "__main__": main()

