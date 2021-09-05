import yfinance as yf


def toStr(x):
    return "{:.2f}".format(x)


class Stock:
    companies = ['AAPL', 'GOOG', 'KO', 'NFLX', 'FB', 'MSFT', 'V', 'BRB-K']

    def getCurrentPrices(self):
        map_to_price = {}
        for company in self.companies:
            stock = yf.Ticker(company)
            # price = stock.info['regularMarketPrice']
            price = stock.info['bid']
            map_to_price[company] = price
        return map_to_price

    def getPrices5DaysAgo(self):
        map_to_price = {}
        for company in self.companies:
            stock = yf.Ticker(company)
            hist = stock.history(period="1mo", interval="1d")
            price_week_ago = hist['Open'][len(hist) - 5]
            map_to_price[company] = price_week_ago
        return map_to_price

    def getCurrentPricesWithPrevious(self):
        prev_price = self.getPrices5DaysAgo()
        prices = self.getCurrentPrices()
        l = []
        for company, now_price in prices.items():
            old_price = prev_price[company]
            percent = ((now_price / old_price) - 1) * 100
            str_percent = toStr(percent)
            if percent > 0:
                str_percent = "✅+" + str_percent
            else:
                str_percent = "⛔️" + str_percent
            l.append(
                company + " 1w ago: " + toStr(prev_price[company]) + ", now: " + toStr(
                    now_price) + "\ndiff: " + str_percent)
        return l
