# Generated by Django 3.0.6 on 2020-06-01 14:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0021_stock_trade_trade'),
    ]

    operations = [
        migrations.AddField(
            model_name='h_stock',
            name='stock_company',
            field=models.ForeignKey(default='1', on_delete=django.db.models.deletion.CASCADE, to='stock.Stock_Company'),
        ),
    ]
