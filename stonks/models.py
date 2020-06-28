from django.db import models

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
        ('IBN', 'Icici Bank Ltd	')
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



class SymbolApiHistory(models.Model):
    '''
        Modelo para controle da atualização dos valores recebidos da API AlphaVantage.
    '''

    date = models.DateField(
        auto_now=True
        )
    
    author = models.ForeignKey(
        'user_control.Pessoa', 
        blank=True, null=True, 
        on_delete=models.PROTECT
        )
    
