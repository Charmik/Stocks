import urllib
import os
import pandas as pd
import yfinance as yf
from urllib.error import HTTPError
from get_all_tickers import get_tickers as gt
from telegram_bot import sendMessage
from telegram_bot import init_telegram_bot


def main():
    init_telegram_bot()
    find_new_reports()


def find_new_reports():
    with open('tickets.txt') as f:
        lines = [line.rstrip() for line in f]

    while True:
        out = open("out.txt", "w")
        out.write("Started test\n")
        for ticker_str in lines:
            success = True
            try:
                print("analyze: ", ticker_str)
                ticker = yf.Ticker(ticker_str)
                info = ticker.info
                earnings = ticker.earnings

                out.write(ticker_str + "\n")
                out.flush()
                write_quarter(ticker, ticker_str)
            except KeyError:
                success = False
            except IndexError:
                success = False
            except ValueError:
                success = False
            # except Exception as e:
            except urllib.error.HTTPError:
                success = False
        out.close()


def write_quarter(ticker, ticker_str):
    quarterly_earning_str = str(ticker.quarterly_earnings)
    data_dir = "../../data"
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    ticker_dir = data_dir + "/" + ticker_str
    if not os.path.exists(ticker_dir):
        os.makedirs(ticker_dir)
    finance_file_str = ticker_dir + "/" + "quarter.txt"

    # sendMessage("analyze: " + ticker_str)
    q_name = "4Q2020"
    if q_name in quarterly_earning_str:
        if os.path.exists(finance_file_str):
            with open(finance_file_str, 'r') as f:
                prev = f.read()
                if q_name not in prev:
                    print(ticker_str + " doesn't have 4Q2020")
                    sendMessage(ticker_str + " doesn't have 4Q2020")

    finance_file_out = open(finance_file_str, "w")
    finance_file_out.write(quarterly_earning_str)
    finance_file_out.flush()


def get_all_tickers():
    list_of_tickers = gt.get_tickers()
    gt.get_tickers(NYSE=False, AMEX=False)
    for list_of_ticker in list_of_tickers:
        print(list_of_ticker)


def take_SP500_from_wiki():
    payload = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    first_table = payload[0]
    second_table = payload[1]
    df = first_table
    symbols = df['Symbol'].values.tolist()
    for symbol in symbols:
        print(symbol)


if __name__ == '__main__':
    main()
