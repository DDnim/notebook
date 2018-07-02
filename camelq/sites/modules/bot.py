
import model.market.biyflyer as bitflyer
import model.market.binance as binance
from model.account.account import account
from django.shortcuts import render

def main(request):
    context          = {}
    data = []

    data.append(bitflyer.ticker('BTC_JPY'))
    data.append(binance.ticker('BTCUSDT'))
    context['params'] = data
    #print(data)
    return render(request, 'bot.html', context)