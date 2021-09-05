import os

import tinvest as ti


TOKEN = os.environ['TT']
client = ti.SyncClient(TOKEN)

stocks = client.get_market_stocks()
instruments = stocks.payload.instruments
for instrument in instruments:
    print(instrument.ticker)
