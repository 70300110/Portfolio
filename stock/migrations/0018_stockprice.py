# Generated by Django 3.0.6 on 2020-05-31 13:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0017_auto_20200531_1647'),
    ]

    operations = [
        migrations.CreateModel(
            name='StockPrice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.FloatField()),
                ('datetime', models.DateTimeField(auto_now=True)),
                ('stock', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stock.Stock')),
            ],
        ),
    ]