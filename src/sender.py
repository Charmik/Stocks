import os
import string
from typing import AnyStr
from typing import List

from analyze_result import AnalyzeResult
from telegram_bot import sendMessage


class Sender:
    SP500_COMPANIES_PATH: str = 'data/S&P500_wiki.txt'
    ALWAYS_GOOD_COMPANIES_PATH: str = 'data/good_companies.txt'
    LAST_GOOD_COMPANIES_PATH: str = 'obj/last_good_companies.txt'

    @staticmethod
    def send_result(stocks: List[AnalyzeResult], additional_info: List[AnyStr]):
        Sender.__send_result_to_telegram("📈\n", stocks, additional_info)


        message = "🌈 filtered companies:\n\n"
        always_good_companies = Sender.__get_sp500_companies()
        filtered_results_by_good_companies = [elm for elm in stocks if elm.ticker in always_good_companies]
        Sender.__send_result_to_telegram(message, filtered_results_by_good_companies, additional_info, 10,
                                         update_good_companies_list=False)
        print("send result to telegram")

    @staticmethod
    def __send_result_to_telegram(message: string, stocks: List[AnalyzeResult], additional_info: List[AnyStr],
                                  top_count=20,
                                  update_good_companies_list: bool = True):
        slice_filtered_results: List[AnalyzeResult] = stocks[:top_count]

        current_companies = []
        for stock in slice_filtered_results:
            current_companies.append(stock)

            ticker = stock.ticker
            pe_percent = round(stock.percent_pe_less_than_history, 1)
            ev_to_ebitda_percent = round(stock.percent_ev_to_ebitda_less_than_history, 1)
            pe = round(stock.pe, 1)
            ev_to_ebitda = round(stock.current_ev_over_ebitda, 1)
            message += ticker + '\n' + \
                       "p/e: " + str(pe) + "\n" \
                       + "ev_to_ebitda: " + str(ev_to_ebitda) + "\n" + \
                       "pe_percent: " + str(pe_percent) + "%\n" + \
                       "ev_to_ebitda_percent: " + str(ev_to_ebitda_percent) + "%\n" \
                       + "https://www.macrotrends.net/stocks/charts/" + ticker + "/mohawk-industries/pe-ratio" + "\n\n"
        message = message + '\n' + str(len(stocks)) + ' companies'
        sendMessage(message)
        global_message = ""

        tickers: List[str] = []
        for result in slice_filtered_results:
            tickers.append(result.ticker)

        if update_good_companies_list:
            # show removed companies
            removed_companies = ""
            for old_company in Sender.__get_old_good_companies():
                if old_company not in tickers:
                    removed_companies += old_company + " "
            if len(removed_companies) > 0:
                removed_companies = "❌ removed companies:\n" + removed_companies
                sendMessage(removed_companies)

            # show added companies
            tickers: List[str] = []
            for result in slice_filtered_results:
                tickers.append(result.ticker)

            new_good_companies = Sender.__get_new_good_companies(tickers)
            Sender.__update_good_companies_cache(tickers)
            if len(new_good_companies) > 0:
                global_message = "✅ new companies:\n"
                for new_good_company in new_good_companies:
                    global_message += new_good_company + " "

            if len(global_message) > 0:
                sendMessage(global_message)

    @staticmethod
    def __get_old_good_companies():
        if os.path.exists(Sender.LAST_GOOD_COMPANIES_PATH):
            with open(Sender.LAST_GOOD_COMPANIES_PATH) as fp:
                good_companies: List[string] = fp.readlines()
                for i in range(0, len(good_companies)):
                    good_companies[i] = good_companies[i].strip()
                return good_companies
        return []

    @staticmethod
    def __get_new_good_companies(results: List[str]):
        good_companies = Sender.__get_old_good_companies()
        new_stocks_in_list = []

        for stock in results:
            if stock not in good_companies:
                new_stocks_in_list.append(stock)
        return new_stocks_in_list

    @staticmethod
    def __update_good_companies_cache(results: List[str]):
        if os.path.exists(Sender.LAST_GOOD_COMPANIES_PATH):
            os.remove(Sender.LAST_GOOD_COMPANIES_PATH)
        with open(Sender.LAST_GOOD_COMPANIES_PATH, "w") as fp:
            for stock in results:
                fp.write(stock + "\n")

    @staticmethod
    def __get_always_good_companies() -> List[AnyStr]:
        if os.path.exists(Sender.ALWAYS_GOOD_COMPANIES_PATH):
            with open(Sender.ALWAYS_GOOD_COMPANIES_PATH) as fp:
                good_companies: List[string] = fp.readlines()
                for i in range(0, len(good_companies)):
                    good_companies[i] = good_companies[i].strip()
                return good_companies
        return []

    @staticmethod
    def __get_sp500_companies() -> List[AnyStr]:
        if os.path.exists(Sender.SP500_COMPANIES_PATH):
            with open(Sender.SP500_COMPANIES_PATH) as fp:
                companies: List[string] = fp.readlines()
                for i in range(0, len(companies)):
                    companies[i] = companies[i].strip()
                return companies
        return []
