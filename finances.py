import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta

def get_prices(ticker, date, amount, type):
        stock = yf.Ticker(ticker)
        date_object = datetime.strptime(date, '%d.%m.%Y')
        formatted_date = date_object.strftime('%Y-%m-%d')
        today = datetime.today().strftime("%Y-%m-%d")
        historical_data = stock.history(start=formatted_date, end=today)
        if str(type) == 'BUY':
                close_prices = historical_data['Close']*float(amount)
        else:
                close_prices = historical_data['Close']*float(amount)*-1
        return close_prices

def get_portfolio_prices(historical_prices):
        df = pd.concat(historical_prices, axis=1)
        total_prices = df.sum(axis=1).fillna(0)
        return total_prices

def get_sp_prices(date, price, type):
        sp = yf.Ticker('^GSPC')
        today = datetime.today().strftime("%Y-%m-%d")

        date_object = datetime.strptime(date, '%d.%m.%Y')
        formatted_date = date_object.strftime('%Y-%m-%d')

        historical_data = sp.history(start=formatted_date, end=today)
        if str(type) == 'BUY':
                historical_data['Investment Value'] = historical_data['Close'] / historical_data['Close'].iloc[0] * float(price)
        else:
                historical_data['Investment Value'] = historical_data['Close'] / historical_data['Close'].iloc[0] * float(price) * -1
        historical_data['Close'] = historical_data['Investment Value']
        return historical_data['Close']

def get_difference(portfolio, snp, buy, sell, snp_buy=None, snp_sell=None):
        port_x = buy - sell
        port_y = portfolio.iloc[-1]
        port_diff = port_y - port_x
        port_perc = port_diff / buy * 100
        if snp_buy == None:
                snp_x = port_x
                snp_y = snp.iloc[-1]
                snp_diff = snp_y - snp_x
                snp_perc = snp_diff / buy * 100
        else:
                snp_x = snp_buy - snp_sell
                snp_y = snp.iloc[-1]
                snp_diff = snp_y - snp_x
                snp_perc = snp_diff / snp_buy * 100

        return port_diff, port_perc, snp_diff, snp_perc

def get_portfolio_data(portfolio, table):
        final_prices = []
        new_portfolio = []

        for stock in portfolio:
                ticker = stock['ticker']
                end_date = datetime.today()
                start_date = end_date - timedelta(days=3)
                data = yf.download(ticker, start=start_date.strftime('%Y-%m-%d'), end=end_date.strftime('%Y-%m-%d'))

                if not data.empty:
                        latest_price = data['Close'].iloc[-1]
                        final_prices.append(latest_price)
                else:
                        final_prices.append(None)

                matching_transactions = [t for t in table if t['ticker'] == ticker]

                buy_price = (sum([float(t['price']) for t in matching_transactions if t['type'] == 'BUY']) -
                             sum([float(t['price']) for t in matching_transactions if t['type'] == 'SELL']))

                new_portfolio.append({
                        'ticker': ticker,
                        'amount': stock['amount'],
                        'price': buy_price,
                        'latest_price': final_prices[portfolio.index(stock)] if final_prices else None,
                        'profit': (latest_price - buy_price) * stock['amount'] if latest_price is not None else None
                })

        return new_portfolio



