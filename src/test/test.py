from api.fmg_api import FmgAPI
from stock_history_reader import StockHistoryReader


if __name__ == '__main__':
    history = StockHistoryReader.read_history()
    ticker = "AAPL"
    fb_history = history.get_history(ticker)
    for h in fb_history:
        print(h.date,h.ev_to_ebitda)

    # print("---")
    # current_ev_over_ebitda = FmgAPI.get_key_metrics(ticker)['enterpriseValueOverEBITDATTM']
    # print(current_ev_over_ebitda)
    # data = requests.get(
    #     f"https://financialmodelingprep.com/api/v3/key-metrics-ttm/ABCB?apikey={API_KEY}")
    # data = data.json()
    # print(data[0]['enterpriseValueOverEBITDATTM'])
