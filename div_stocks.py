import pandas as pd
import yfinance as yf

# Web scraping list of S&P 500 Dividend Aristocrats


def load_data():
    url = 'https://en.wikipedia.org/wiki/S%26P_500_Dividend_Aristocrats'
    html = pd.read_html(url, header=0)
    df = html[0]
    return df


df = load_data()

# get stock info

tickers = df['Ticker symbol']

for ticker in tickers:
    info = yf.Ticker(ticker).info
    name = info.get('longName')
    sector = info.get('sector')
    #div = info.get('trailingAnnualDividendYield')
    print(ticker, name, sector)
