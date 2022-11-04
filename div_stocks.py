import pandas as pd
import yfinance as yf
import csv

# Web scraping list of S&P 500 Dividend Aristocrats


def load_data():
    url = 'https://en.wikipedia.org/wiki/S%26P_500_Dividend_Aristocrats'
    html = pd.read_html(url, header=0)
    df = html[0]
    return df


df = load_data()

# get stock info

tickers = df['Ticker symbol']

# current portfolio
details = {'ticker': ['AFL', 'BEN'],
           'price_paid': [59.69, 22.21]}
portfolio_df = pd.DataFrame(details, columns=['ticker', 'price_paid'])

# prepare data set
data = pd.DataFrame(columns=['ticker', 'name', 'sector', 'outstanding', 'price',
                             'capitalization', 'eps', 'price_to_earning_ratio', 'div', 'div_yield', 'div_payout_ratio',
                             'price_paid_for_share', 'yield_on_cost', 'debt_to_equity', 'peg', 'number_of_analysis'])

for ticker in tickers:
    info = yf.Ticker(ticker).info
    name = info.get('longName')
    sector = info.get('sector')
    outstanding = info.get('sharesOutstanding')
    price = info.get('currentPrice')
    capitalization = info.get('marketCap')
    eps = info.get('trailingEps')
    # eps growth rate?
    if price is None or eps is None:
        price_to_earning_ratio = None
    else:
        price_to_earning_ratio = round(price / eps, 2)
    div = info.get('trailingAnnualDividendRate')
    div_yield = info.get('dividendYield')
    # div growth rate?
    div_payout_ratio = info.get('payoutRatio')
    if ticker in portfolio_df.values:
        price_paid_for_share = portfolio_df.loc[portfolio_df['ticker']
                                                == ticker, 'price_paid'].iloc[0]
    else:
        price_paid_for_share = price
    if div is None or price_paid_for_share is None:
        yield_on_cost = None
    else:
        yield_on_cost = round(div / price_paid_for_share, 2)
    debt_to_equity = info.get('debtToEquity')
    # credit rating?
    peg = info.get('pegRatio')
    # div growth streak?
    number_of_analysis = info.get('numberOfAnalystOpinions')

    data = data.append({'ticker': ticker, 'name': name, 'sector': sector, 'outstanding': outstanding, 'price': price,
                        'capitalization': capitalization, 'eps': eps, 'price_to_earning_ratio': price_to_earning_ratio, 'div': div, 'div_yield': div_yield, 'div_payout_ratio': div_payout_ratio,
                        'price_paid_for_share': price_paid_for_share, 'yield_on_cost': yield_on_cost, 'debt_to_equity': debt_to_equity, 'peg': peg, 'number_of_analysis': number_of_analysis}, ignore_index=True)

# export dataset to CSV file
data.to_csv('data.csv')
