from google.oauth2.service_account import Credentials
import gspread
import finances
import pyqtgraph as pg
import matplotlib.dates as mdates
import pandas as pd
from datetime import datetime, timedelta


def read_table(spreadsheet_id):
    credentials = Credentials.from_service_account_file("key.json", scopes=[
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive'
    ])
    gc = gspread.authorize(credentials)
    worksheet = gc.open_by_key(spreadsheet_id).worksheet("List 1")
    data_range = worksheet.get('A2:E')
    headers = data_range[0]
    return [{headers[i]: row[i] for i in range(len(headers))} for row in data_range[1:]]

def get_id(link):
    return link.replace('https://docs.google.com/spreadsheets/d/', '').replace('/edit?gid=0#gid=0', '')

def create_graph_widget(investment_data, sp500_data):
    investment_df = pd.DataFrame(investment_data).rename(columns={0: 'Date', 1: 'Price'})
    sp500_df = pd.DataFrame(sp500_data).rename(columns={0: 'Date', 1: 'Price'})
    investment_df['Date'] = pd.to_datetime(investment_df['Date']).dt.tz_localize(None)
    sp500_df['Date'] = pd.to_datetime(sp500_df['Date']).dt.tz_localize(None)
    investment_df['Date_num'] = mdates.date2num(investment_df['Date'])
    sp500_df['Date_num'] = mdates.date2num(sp500_df['Date'])
    plot_widget = pg.PlotWidget()
    plot_widget.plot(investment_df['Date_num'], investment_df['Price'], pen='blue', name='Investment')
    plot_widget.plot(sp500_df['Date_num'], sp500_df['Price'], pen='white', name='S&P 500')
    ticks = [(mdates.date2num(investment_df['Date'][i]), investment_df['Date'][i].strftime('%Y-%m-%d')) for i in range(0, len(investment_df), 3)]
    plot_widget.getAxis('bottom').setTicks([ticks])
    return plot_widget

def get_data_for_graph(id, date):
    table = read_table(id)
    stock_info, snp_info = [], []
    buy, sell = 0, 0
    for stock in table:
        stock_info.append(finances.get_prices(stock['ticker'], stock['date'], stock['amount'], stock['type']))
        if stock['type'] == 'BUY':
            buy += float(stock['price'])
        else:
            sell += float(stock['price'])
        snp_info.append(finances.get_sp_prices(stock['date'], stock['price'], stock['type']))
    invest_list = finances.get_portfolio_prices(snp_info)
    portfolio_prices = pd.DataFrame(finances.get_portfolio_prices(stock_info)).tz_localize(None)
    snp_prices = pd.DataFrame(finances.get_portfolio_prices(snp_info)).tz_localize(None)
    filtered_pt = portfolio_prices[portfolio_prices.index >= date]
    filtered_snp = snp_prices[snp_prices.index >= date]

    if date != datetime(1900, 1, 1):
        sell, buy = 0, filtered_pt.iloc[0][0]
        snp_sell, snp_buy = 0, filtered_snp.iloc[0][0]
        for stock in table:
            stock_date = datetime.strptime(stock['date'], '%d.%m.%Y')
            if stock['type'] == 'SELL' and stock_date > date + timedelta(days=1):
                sell += float(stock['price'])
                snp_sell += -filtered_snp.loc[stock_date][0] + filtered_snp.loc[stock_date - timedelta(days=1)][0]
            if stock['type'] == 'BUY' and stock_date > date + timedelta(days=1):
                buy += float(stock['price'])
                snp_buy += filtered_snp.loc[stock_date][0] - filtered_snp.loc[stock_date - timedelta(days=1)][0]
        return filtered_pt, filtered_snp, buy, sell, invest_list, snp_buy, snp_sell

    return filtered_pt, filtered_snp, buy, sell, invest_list