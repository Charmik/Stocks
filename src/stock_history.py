import datetime
from typing import List, Dict, KeysView


class StockHistory:
    class Metrics:
        def __init__(self, symbol, date: datetime.datetime, net_income, operating_income, eps, p_to_fcf, roe, roa, div_yield,
                     net_profit_margin,
                     p_to_b, p_to_e, peg, p_to_s, ev_to_ebitda, ev_to_ebit, ev_to_fcf, ev_to_s, rsi):
            self.symbol = symbol
            self.date = date
            self.net_income = net_income
            self.operating_income = operating_income
            self.eps = eps
            self.p_to_fcf = p_to_fcf
            self.roe = roe
            self.roa = roa
            self.div_yield = div_yield
            self.net_profit_margin = net_profit_margin
            self.p_to_b = p_to_b
            self.p_to_e = p_to_e
            self.peg = peg
            self.p_to_s = p_to_s
            self.ev_to_ebitda = ev_to_ebitda
            self.ev_to_ebit = ev_to_ebit
            self.ev_to_fcf = ev_to_fcf
            self.ev_to_s = ev_to_s
            self.rsi = rsi

        def __str__(self) -> str:
            return self.symbol + self.date + self.net_income + self.eps + self.p_to_fcf + self.roe + self.roa + self.div_yield + self.net_profit_margin + \
                   self.p_to_b + self.p_to_e + self.peg + self.p_to_s + self.ev_to_ebitda + self.ev_to_ebit + self.ev_to_fcf + self.ev_to_s + self.rsi


    ticker_to_history: Dict[str, List[Metrics]]

    def __init__(self):
        self.ticker_to_history = {}

    def add_history(self, stock, metrics_list: List[Metrics]):
        self.ticker_to_history[stock] = metrics_list

    def get_history(self, stock) -> List[Metrics]:
        return self.ticker_to_history[stock]

    def get_tickers(self) -> KeysView[str]:
        return self.ticker_to_history.keys()
