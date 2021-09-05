import os
from decimal import *

import tinvest as ti

balance = {}


def update_balance(value, currency):
    if not currency in balance:
        balance[currency] = Decimal(0)
    balance[currency] += value


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
    balance = {}
    response = client.get_portfolio(broker_account_id=broker_account_id)  # tinvest.PortfolioResponse
    for pos in response.payload.positions:
        currency = pos.average_position_price.currency
        value = pos.average_position_price.value * pos.balance + pos.expected_yield.value
        if pos.instrument_type in [ti.InstrumentType.stock, ti.InstrumentType.bond, ti.InstrumentType.etf]:
            pass
        elif pos.instrument_type == ti.InstrumentType.currency:
            # Skip "currencies"
            continue
        else:
            print("  pos:", pos)

        # Update balance
        update_balance(value, currency)
        print(f"  {pos.name} {value}")

    print("  ---------------------------------------")
    responce = client.get_portfolio_currencies(broker_account_id=broker_account_id)
    for cpos in responce.payload.currencies:
        update_balance(cpos.balance, cpos.currency)
        print(f"  {cpos.currency}={cpos.balance}")
    print("  =============== TOTAL =================")
    for currency, value in balance.items():
        print(f"  {currency} {value}")
    print("")
