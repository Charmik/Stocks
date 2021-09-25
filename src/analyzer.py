import datetime
import string
from typing import List

from stock_history import StockHistory


class Analyzer:

    def __init__(self, stock: string, metrics: List[StockHistory.Metrics], end_time: datetime.datetime, years: int):
        start_date: datetime.datetime = end_time - datetime.timedelta(days=years * 365)

        filtered_by_time: List[StockHistory.Metrics] = []
        for metric in metrics:
            if metric.date < start_date:
                continue
            if metric.date > end_time:
                break
            filtered_by_time.append(metric)

        self.ticker = stock
        self.metrics = filtered_by_time
        self.years = years

    def analyze(self) -> bool:  # true if good company, false otherwise
        res_net_income: bool = Analyzer.NetIncomeFilter().filter(self.ticker, self.metrics, self.years)
        res_eps: bool = Analyzer.EpsFilter().filter(self.ticker, self.metrics, self.years)

        if res_net_income and res_eps is True:
            print(self.ticker, "was approved")
            return True

        return False

    def get_percent_pe_less_than_history(self, current_pe: float) -> float:
        pes = []
        for metric in self.metrics:
            pes.append(metric.p_to_e)
        pes = sorted(pes)
        percent = 100
        for j in range(len(pes)):  # can be binary search
            if pes[j] > current_pe:
                percent = (float(j) / len(pes)) * 100
                break
        return percent

    def get_percent_ev_to_ebitda_less_than_history(self, ev_to_ebitda: float) -> float:
        ev_to_ebitda_history = []
        for metric in self.metrics:
            ev_to_ebitda_history.append(metric.ev_to_ebitda)
        ev_to_ebitda_history = sorted(ev_to_ebitda_history)
        percent = 100
        for j in range(len(ev_to_ebitda_history)):  # can be binary search
            if ev_to_ebitda_history[j] > ev_to_ebitda:
                percent = (float(j) / len(ev_to_ebitda_history)) * 100
                break
        return percent


    class Filter:
        # change return value - if it's possible to make chains
        def filter(self, stock: string, metrics: List[StockHistory.Metrics], years: int) -> bool:
            pass

        @staticmethod
        def filter_by_percent_growth(ticker: string, years, array: [float], less_than_prev_year_percent=15,
                                     grown_per_year_percent=17):
            if len(array) < years:
                # print(stock, "skip cause of len of", stock)
                return False

            array = array[0:years]

            for i in range(0, len(array)):
                # fix these ugly ifs
                if array[i] is None:
                    array[i] = 0
                if array[i] < 0:
                    array[i] = 0

            less_than_prev_count = 0
            for i in range(1, len(array)):
                if array[i] <= array[i - 1]:  # = for zeros
                    less_than_prev_count += 1
            percent = 0
            if len(array) > 0:
                percent = float(less_than_prev_count) / len(array) * 100
            if percent > less_than_prev_year_percent:
                # print("skip cause of percent less than prev: ", stock, percent, less_than_prev_year_percent)
                return False

            # check how fast array grown
            base = array[0]
            for i in range(1, years):
                base = base + (base / 100 * grown_per_year_percent)
                if base == 0:
                    base = array[i]
            # check how fast it grows
            if base > array[years - 1]:
                # print(stock, "skip cause of % of growth base:", base, array)
                return False

            # print(stock, "base: ", base, " real: ", array[years - 1])
            return True


    class NetIncomeFilter(Filter):

        def filter(self, ticker: string, metrics: List[StockHistory.Metrics], years: int) -> bool:
            net_income = []
            for metric in metrics:
                # net_income.append(getattr(metric, 'net_income'))
                net_income.append(metric.net_income)
            return self.filter_by_percent_growth(ticker, years, net_income)


    class EpsFilter(Filter):

        def filter(self, ticker: string, metrics: List[StockHistory.Metrics], years: int) -> bool:
            eps = []
            for metric in metrics:
                # eps.append(getattr(metric,'eps'))
                eps.append(metric.eps)
            return self.filter_by_percent_growth(ticker, years, eps)
