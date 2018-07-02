from market_api.bitflyer import bitflyer

bitflyer = bitflyer()
print(bitflyer.get_executions('BTC_JPY'))
print(bitflyer.get_ticker('BTC_JPY'))
print(bitflyer.get_balance())


