import os
from datetime import datetime, timezone, timedelta

import tinvest as ti
from tinvest import Currency, InstrumentType, OperationTypeWithCommission


class Stock:

    def __init__(self, ticker, value, currency, figi):
        self.ticker = ticker
        self.value = value
        self.currency = currency
        self.figi = figi


figi_to_stock = {}


def update_map(ticker, value, currency, figi):
    if not figi in figi_to_stock:
        figi_to_stock[figi] = Stock(ticker, value, currency, figi)
    else:
        figi_to_stock[figi].value += value


TOKEN = os.environ['TT']
client = ti.SyncClient(TOKEN)

# stocks = client.get_market_stocks()
# instruments = stocks.payload.instruments
# for instrument in instruments:
#     print(instrument.ticker)


for account in client.get_accounts().payload.accounts:
    broker_account_type = account.broker_account_type
    broker_account_id = account.broker_account_id
    print(f"broker_account_id={broker_account_id} broker_account_type={broker_account_type}")

    # Reset balance
    figi_to_stock = {}

    response = client.get_portfolio(broker_account_id=broker_account_id)  # tinvest.PortfolioResponse
    for pos in response.payload.positions:
        currency = pos.average_position_price.currency
        value = pos.average_position_price.value * pos.balance + pos.expected_yield.value
        figi = pos.figi
        if pos.instrument_type in [ti.InstrumentType.stock, ti.InstrumentType.bond, ti.InstrumentType.etf]:
            pass
        elif pos.instrument_type == ti.InstrumentType.currency:
            # Skip "currencies"
            continue
        else:
            print("  pos:", pos)

        # Update balance
        update_map(pos.name, value, currency, figi)

    print("  ---------------------------------------")

    for figi, stock in figi_to_stock.items():
        print(f" {stock.figi} {stock.ticker} {stock.value}")

    dt_format = lambda x: x.replace(tzinfo=timezone.utc).isoformat()
    from_time = dt_format((datetime.now() - timedelta(days=365 * 10)))
    to_time = dt_format(datetime.now())
    operations = client.get_operations(from_time, to_time, broker_account_id=broker_account_id).payload.operations

    operations = [elm for elm in operations if
                  elm.currency == Currency.usd and elm.instrument_type == InstrumentType.stock and elm.operation_type == OperationTypeWithCommission.buy]

    for operation in operations:
        print(operation.figi)

    print("")
