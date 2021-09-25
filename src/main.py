import datetime
import os
from typing import List

from analyze_result import AnalyzeResult
from analyzer import Analyzer
# from cache import Cache
from api.fmg_api import FmgAPI
from sender import Sender
from stock_history_reader import StockHistoryReader
from telegram_bot import init_telegram_bot


'''
tasks:
-) post when `choosen` companies lost more than 3% of price for day
-) print by query /get
-) parse macrotrends (or any other) & compare P/E (take trailing p/e only)
-) simulation of algorithm from random data in the past & show profit from strategy
'''

init_telegram_bot()


def read_good_companies():
    with open("data/good_companies.txt") as fp:
        symbols: [str] = fp.readlines()
        symbols = [x.rstrip() for x in symbols]
        return symbols


def start():
    years = 15
    history = StockHistoryReader.read_history()
    tickers = history.get_tickers()

    result: List[AnalyzeResult] = []
    for ticker in tickers:
        now = datetime.datetime.now()  # be able to change this
        analyzer = Analyzer(ticker, history.get_history(ticker), now, years)
        is_good_company = analyzer.analyze()
        if is_good_company is True:
            pe: float = FmgAPI.get_quote_metrics(ticker)['pe']
            if pe is None or pe > 40:
                continue
            percent_pe_less_than_history = analyzer.get_percent_pe_less_than_history(pe)

            current_ev_over_ebitda = FmgAPI.get_key_metrics(ticker)['enterpriseValueOverEBITDATTM']
            if current_ev_over_ebitda is None:
                current_ev_over_ebitda = 100
            percent_ev_to_ebitda_less_than_history = analyzer.get_percent_ev_to_ebitda_less_than_history(
                current_ev_over_ebitda)

            analyze_result = AnalyzeResult(ticker, pe, percent_pe_less_than_history, current_ev_over_ebitda,
                                           percent_ev_to_ebitda_less_than_history)  # be able to get the old one
            result.append(analyze_result)

    print("Analysis is processed")

    result = sorted(result,
                    key=lambda cur: (cur.percent_pe_less_than_history is None, cur.percent_pe_less_than_history))
    # result = sorted(result, key=lambda cur: (
    #     cur.percent_ev_to_ebitda_less_than_history is None, cur.percent_ev_to_ebitda_less_than_history))

    for res in result:
        print(res.ticker, res.pe, res.percent_pe_less_than_history, res.current_ev_over_ebitda,
              res.percent_ev_to_ebitda_less_than_history)

    additional_info = []
    for ticker in result:
        additional_info.append("some additional info will be here later")

    Sender.send_result(result, additional_info)


if __name__ == '__main__':
    print("start main")
    print("FINANCIAL_MODELING_GREP_API:", os.environ['FINANCIAL_MODELING_GREP_API'])
    try:
        start()
    except:
        var = traceback.format_exc()
        print("Whew!", var, "occurred.")
    finally:
        print("Finished")
        os._exit(0)
