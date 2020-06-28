from django.core.management.base import BaseCommand, CommandError
from stonks.models import StockExchangeSymbol

class Command(BaseCommand):
    help = "Comando para popular o banco com a base de Symbols selecionados no modelo de StockExchangeSymbol"

    def handle(self, *args, **options):
        try:
            available_symbols = StockExchangeSymbol.AVAILABLE_SYMBOLS
            for symbol in available_symbols:
                already_in_db = StockExchangeSymbol.objects.filter(
                    symbol=symbol[0],
                    name=symbol[1]
                ).exists()

                if not already_in_db:
                    StockExchangeSymbol.objects.create(
                        symbol=symbol[0],
                        name=symbol[1]
                    )
        except:
            raise CommandError('Houve um problema.')