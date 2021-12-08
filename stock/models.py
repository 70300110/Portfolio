from django.db import models

CHOICES = ( (1, 'YES'), (2, 'NO') )
class Bank(models.Model):
    name = models.CharField(max_length = 50)
    real = models.IntegerField(choices = CHOICES, default=0)
    datetime = models.DateTimeField(auto_now = True)

    def __str__(self):
        return self.name

class BankDeposit(models.Model):
    bank = models.ForeignKey(Bank, on_delete = models.CASCADE)
    jpy_deposit = models.FloatField()
    usd_deposit = models.FloatField()
    datetime = models.DateTimeField(auto_now = True)

    def __str__(self):
        return self.bank.name + " [Deposit]"

class Stock_Company(models.Model):
    name = models.CharField(max_length = 50)
    account = models.CharField(max_length = 50)
    real = models.IntegerField(choices = CHOICES, default=0)
    datetime = models.DateTimeField(auto_now = True)

    def __str__(self):
        return self.name + " [" + self.account + "]"

class Stock_CompanyDeposit(models.Model):
    stock_comp = models.ForeignKey(Stock_Company, on_delete = models.CASCADE)
    jpy_deposit = models.FloatField()
    usd_deposit = models.FloatField()
    datetime = models.DateTimeField(auto_now = True)

    def __str__(self):
        return self.stock_comp.name + " [" + self.stock_comp.account + "]"

COUNTRY_CHOICES = ( (1, 'JAPAN'), (2, 'USA') )

class Stock(models.Model):
    name = models.CharField(max_length = 50)
    code = models.CharField(max_length = 10)
    country = models.IntegerField(choices = COUNTRY_CHOICES, default=0)
    datetime = models.DateTimeField(auto_now = True)

    def __str__(self):
        return self.name

class StockPrice(models.Model):
    stock = models.ForeignKey(Stock, on_delete = models.CASCADE)
    price = models.FloatField()
    datetime = models.DateTimeField(auto_now = True)

    def __str__(self):
        return self.stock.name + "[Price]"

class H_Stock(models.Model):
    stock = models.ForeignKey(Stock, on_delete = models.CASCADE)
    stock_company = models.ForeignKey(Stock_Company, on_delete = models.CASCADE, default='1')
    price_ave = models.FloatField()
    quantity = models.IntegerField()
    datetime = models.DateTimeField(auto_now = True)

    def __str__(self):
        return self.stock.name + " [H]"

class User(models.Model):
    name = models.CharField(max_length = 50)
    password = models.CharField(max_length = 50)

    def __str__(self):
        return self.name

class Portfolio(models.Model):
    name = models.CharField(max_length = 50)
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    stock_company = models.ForeignKey(Stock_Company, on_delete = models.CASCADE)
    h_stock = models.ForeignKey(H_Stock, on_delete = models.CASCADE)
    datetime = models.DateTimeField(auto_now = True)

    def __str__(self):
        return self.name

CURRENCY_CHOICES = ( (1, 'JPY'), (2, 'USD') )

class Bank_Trade(models.Model):
    name = models.CharField(max_length = 50)
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    inbank = models.ForeignKey(Bank, on_delete = models.CASCADE, related_name = "inbank")
    outbank = models.ForeignKey(Bank, on_delete = models.CASCADE, related_name = "outbank")
    currency = models.IntegerField(choices = CURRENCY_CHOICES, default=0)
    price = models.FloatField()
    fee = models.FloatField()
    datetime = models.DateTimeField(auto_now = True)

    def __str__(self):
        return "Bank Trade" + str(self.id)

TRADE_CHOICES = ( (1, 'BUY'), (2, 'SELL') )

class Stock_Trade(models.Model):
    name = models.CharField(max_length = 50)
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    h_stock = models.ForeignKey(H_Stock, on_delete = models.CASCADE)
    trade = models.IntegerField(choices = TRADE_CHOICES, default=0)
    fee = models.FloatField()
    tax = models.FloatField()
    datetime = models.DateTimeField(auto_now = True)

    def __str__(self):
        return "Stock Trade" + str(self.id)
