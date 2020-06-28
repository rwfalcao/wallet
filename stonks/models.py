import datetime

from django.db import models
from django.db import transaction
from stonks.services import AlphaVantageWrapper


class StockExchangeSymbol(models.Model):
    '''
        Modelo para os possíveis symbols disponíveis.
    '''


    AVAILABLE_SYMBOLS = [
        ('IAA', 'Iaa Inc'),
        ('IAE', 'VOYA Asia Pacific High Dividend Equity'),
        ('IAG', 'Iamgold Corp'),
        ('IBA', 'Industrias Bachoco'),
        ('IBM', 'International Business Machines'),
    ]

    symbol = models.CharField(
        'Símbolo',
        max_length=10,
        null=False
        )
    
    name = models.CharField(
        'Primeiro nome',
        max_length=200,
        null=False
        )

    def __str__(self):
        return '%s: %s' % (self.symbol, self.name)

    
    def already_fetched_today(self):
        return self.dailysymbolinformation_set.filter(
            history__date=datetime.datetime.now().date()
        ).exists()

    @transaction.atomic
    def update_daily_time_series(self):
        av_wrapper = AlphaVantageWrapper()
        if not self.already_fetched_today():
            request_content = av_wrapper.get_daily_time_series(self.symbol)

            history = SymbolApiHistory.objects.create(
                date=datetime.datetime.now().date()
            )

            daily_symbol_info = DailySymbolInformation.objects.create(
                history=history,
                information=request_content['Meta Data']['1. Information'] if request_content['Meta Data']['1. Information'] else '',
                output_size=request_content['Meta Data']['4. Output Size'] if request_content['Meta Data']['4. Output Size'] else '',
                last_refreshed=request_content['Meta Data']['3. Last Refreshed'] if request_content['Meta Data']['3. Last Refreshed'] else datetime.datetime.now().date(),
                symbol=self
            )

            daily_values = request_content.get('Time Series (Daily)')
            for date, values in daily_values.items():
                date_format = datetime.datetime.strptime(date, "%Y-%m-%d").date()

                date_already_in_db = DailySymbolTimeSerie.objects.filter(
                    symbol_information__symbol=self,
                    date=date_format
                ).exists()

                if not date_already_in_db:
                    DailySymbolTimeSerie.objects.create(
                        symbol_information=daily_symbol_info,
                        date=date_format,
                        open_price=values.get('1. open') if values.get('1. open') else 0,
                        high=values.get('2. high') if values.get('2. high') else 0,
                        low=values.get('3. low') if values.get('3. low') else 0,
                        close=values.get('4. close') if values.get('4. close') else 0,
                        volume=values.get('5. volume') if values.get('5. volume') else 0
                    )


        return False

    def get_latest_daily_information(self):
        latest_dailies = DailySymbolTimeSerie.objects.filter(
            symbol_information__symbol=self
        ).order_by(
            '-date'
        )[:5]
        return latest_dailies

    def get_latest_closing_information(self):
        return self.get_latest_daily_information().first()



class SymbolApiHistory(models.Model):
    '''
        Modelo para controle da atualização dos valores recebidos da API AlphaVantage.
    '''

    date = models.DateField(
        auto_now=True
        )
    

class DailySymbolInformation(models.Model):
    '''
        Modelo para controle da atualização dos valores recebidos da API AlphaVantage.
    '''

    history = models.ForeignKey(
        'stonks.SymbolApiHistory', 
        blank=True, null=True, 
        on_delete=models.CASCADE
        )

    information = models.CharField(
        'Information',
        max_length=500,
        null=False
        )

    output_size = models.CharField(
        'Output size',
        max_length=100,
        null=False
        )
    
    symbol = models.ForeignKey(
        'stonks.StockExchangeSymbol', 
        blank=True, null=True, 
        on_delete=models.CASCADE
        )

    last_refreshed = models.DateField(
        'Last Refreshed',
        )

    
class DailySymbolTimeSerie(models.Model):
    '''
        Modelo para controle da atualização dos valores recebidos da API AlphaVantage.
    '''

    symbol_information = models.ForeignKey(
        'stonks.DailySymbolInformation', 
        blank=True, null=True, 
        on_delete=models.CASCADE
        )

    date = models.DateField()

    open_price = models.DecimalField(
        max_digits=12, 
        decimal_places=4
        )
    
    high = models.DecimalField(
        max_digits=12, 
        decimal_places=4
        )

    low = models.DecimalField(
        max_digits=12, 
        decimal_places=4
        )

    close = models.DecimalField(
        max_digits=12, 
        decimal_places=4
        )

    volume = models.DecimalField(
        max_digits=12, 
        decimal_places=4
        )

    def ended_higher(self):
        return True if self.close > self.open_price else False

    
class UserWallet(models.Model):
    '''
        Modelo que representa a carteira do User
    '''

    owner = models.ForeignKey(
        'user_control.Pessoa', 
        on_delete=models.CASCADE
        )

    balance = models.DecimalField(
        max_digits=12, 
        decimal_places=2
        )
    
    def __str__(self):
        return "%s's Wallet" % (self.owner.first_name)

    def get_purchases(self):
        return self.purchase_set.all()

    @transaction.atomic
    def purchase_symbol(self, symbol):
        '''
            Lógica para compra de symbol.
        '''

        latest_info = symbol.get_latest_closing_information()

        last_close_price = 0 
        if latest_info:
            last_close_price = latest_info.close

        Purchase.objects.create(
            wallet=self,
            symbol=symbol,
            amount=last_close_price,
            current_daily=latest_info
        )

        self.balance += last_close_price
        self.save()


class Purchase(models.Model):
    wallet = models.ForeignKey(
        'stonks.UserWallet', 
        on_delete=models.CASCADE
        )
    
    symbol = models.ForeignKey(
        'stonks.StockExchangeSymbol', 
        on_delete=models.CASCADE
        )

    amount = models.DecimalField(
        max_digits=12, 
        decimal_places=2
        )
    
    current_daily = models.ForeignKey(
        'stonks.DailySymbolTimeSerie', 
        on_delete=models.CASCADE
        )

    date_time = models.DateTimeField(
        auto_now=True
    )


