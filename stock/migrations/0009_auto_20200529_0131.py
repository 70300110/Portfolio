# Generated by Django 3.0.6 on 2020-05-28 16:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0008_bank_trade'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bank',
            old_name='updated_datetime',
            new_name='datetime',
        ),
    ]
