from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from stonks.services import AlphaVantageWrapper

from stonks.models import SymbolApiHistory, StockExchangeSymbol

@login_required()
def index(request):
    av_wrapper = AlphaVantageWrapper()
    return render(request, 'index.html')
