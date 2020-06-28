import datetime

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from stonks.models import SymbolApiHistory, StockExchangeSymbol, SymbolApiHistory, DailySymbolInformation


@login_required()
def index(request):
    '''
        View para página principal do sistema.
    '''
    available_symbols = StockExchangeSymbol.AVAILABLE_SYMBOLS
    for symbol in available_symbols:
        symbol_code = symbol[0]

        symbol_obj = StockExchangeSymbol.objects.filter(
            symbol=symbol_code
        ).first()

        already_fetched_today = symbol_obj.already_fetched_today()

        if not already_fetched_today:
            res = symbol_obj.update_daily_time_series()
    
    wallet = request.user.pessoa.get_wallet()
    context = {
        'wallet': wallet,
        'purchases': wallet.get_purchases()
    }

    return render(request, 'index.html', context)

@login_required()
def available_symbols_list(request):
    '''
        View para a listagem de symbols.
    '''
    value_entered = 0
    if request.method == 'POST':
        request.POST.get('money-value')
        value_entered = float(request.POST.get('money-value').replace('.', '').replace(',', '.'))

    context = {
        'symbols': StockExchangeSymbol.objects.all(),
        'value_entered': value_entered
    }
    return render(request, 'available_symbols_list.html', context)

@login_required()
def buy_symbol(request, pk):
    '''
        View com a lógica da compra de symbol.
    '''
    symbol = StockExchangeSymbol.objects.filter(pk=pk).first()
    wallet = request.user.pessoa.get_wallet()

    wallet.purchase_symbol(symbol)

    return redirect('/')




