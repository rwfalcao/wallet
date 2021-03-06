# Generated by Django 2.2.13 on 2020-06-28 23:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('stonks', '0008_auto_20200628_1642'),
    ]

    operations = [
        migrations.CreateModel(
            name='Purchase',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=12)),
                ('current_daily', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stonks.DailySymbolTimeSerie')),
                ('symbol', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stonks.StockExchangeSymbol')),
                ('wallet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stonks.UserWallet')),
            ],
        ),
    ]
