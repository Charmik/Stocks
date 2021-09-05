import csv
from datetime import datetime
from typing import List

from stock_history import StockHistory


class StockHistoryReader:
    REPORT_PATH_STR: str = 'data/report.csv'

    @staticmethod
    def str_to_float(s: str):
        if s == '':
            return 0
        return float(s)

    @staticmethod
    def read_history():
        with open(StockHistoryReader.REPORT_PATH_STR) as csvfile:
            csv_reader = csv.reader(csvfile, delimiter=',')
            next(csv_reader, None)  # skip header

            # symbol,date,net_income,eps,p_to_fcf,roe,roa,div_yield,net_profit_margin,p_to_b,p_to_e,peg,p_to_s,ev_to_ebitda,ev_to_ebit,ev_to_fcf,ev_to_s,rsi
            prev_symbol = "X@X@X@X@X"
            metrics_for_current_symbol: List[StockHistory.Metrics] = []
            history: StockHistory = StockHistory()

            for row in csv_reader:
                symbol = row[0]
                date = datetime.fromisoformat(row[1])
                net_income = float(row[2])
                operating_income = float(row[3])
                eps = StockHistoryReader.str_to_float(row[4])
                p_to_fcf = StockHistoryReader.str_to_float(row[5])
                roe = StockHistoryReader.str_to_float(row[6])
                roa = StockHistoryReader.str_to_float(row[7])
                div_yield = StockHistoryReader.str_to_float(row[8])
                net_profit_margin = StockHistoryReader.str_to_float(row[9])
                p_to_b = StockHistoryReader.str_to_float(row[10])
                p_to_e = StockHistoryReader.str_to_float(row[11])
                peg = StockHistoryReader.str_to_float(row[12])
                p_to_s = StockHistoryReader.str_to_float(row[13])
                ev_to_ebitda = StockHistoryReader.str_to_float(row[14])
                ev_to_ebit = StockHistoryReader.str_to_float(row[15])
                ev_to_fcf = StockHistoryReader.str_to_float(row[16])
                ev_to_s = StockHistoryReader.str_to_float(row[17])
                rsi = StockHistoryReader.str_to_float(row[18])

                metrics = StockHistory.Metrics(symbol, date, net_income, operating_income, eps, p_to_fcf, roe, roa,
                                               div_yield,
                                               net_profit_margin,
                                               p_to_b, p_to_e, peg, p_to_s, ev_to_ebitda, ev_to_ebit, ev_to_fcf,
                                               ev_to_s, rsi)

                if prev_symbol == "X@X@X@X@X":
                    prev_symbol = symbol
                if symbol != prev_symbol:
                    # prev_symbol = metrics_for_current_symbol[0].symbol
                    history.add_history(prev_symbol, metrics_for_current_symbol)
                    metrics_for_current_symbol = []
                    prev_symbol = symbol
                metrics_for_current_symbol.append(metrics)
            if len(metrics_for_current_symbol) > 0:
                history.add_history(metrics_for_current_symbol[0].symbol, metrics_for_current_symbol)

            return history
