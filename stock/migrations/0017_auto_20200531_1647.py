# Generated by Django 3.0.6 on 2020-05-31 07:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0016_stock_companydeposit'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='stock_company',
            name='jpy_deposit',
        ),
        migrations.RemoveField(
            model_name='stock_company',
            name='usd_deposit',
        ),
    ]