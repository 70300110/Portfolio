from django.forms import ModelForm, TextInput, Select
from .models import Bank, BankDeposit, Stock_Company, Stock_CompanyDeposit, Stock, StockPrice, H_Stock, User, Portfolio, Bank_Trade, Stock_Trade

class BankForm(ModelForm):
    class Meta:
        model = Bank
        fields = { 'name', 'real' }
        widgets = {
            'name' : TextInput(attrs={'class' : 'form-control', 'placeholder' : 'Bank_Name'}),
            'real' : Select(attrs={'class' : 'form-control', 'placeholder' : 'Real?'}),
        }

class BankDepositForm(ModelForm):
    class Meta:
        model = BankDeposit
        fields = { 'bank', 'jpy_deposit', 'usd_deposit'}
        widgets = {
            'bank' : Select(attrs={'class' : 'form-control', 'placeholder' : '  Bank'}),
            'jpy_deposit' : TextInput(attrs={'class' : 'form-control', 'placeholder' : 'JPY_DEPOSIT'}),
            'usd_deposit' : TextInput(attrs={'class' : 'form-control', 'placeholder' : 'USD_DEPOSIT'}),
        }

class Stock_CompanyForm(ModelForm):
    class Meta:
        model = Stock_Company
        fields = { 'name', 'account', 'real'}
        widgets = {
            'name' : TextInput(attrs={'class' : 'form-control', 'placeholder' : 'Stock_CompanyName'}),
            'account' : TextInput(attrs={'class' : 'form-control', 'placeholder' : 'Account'}),
            'real' : Select(attrs={'class' : 'form-control', 'placeholder' : 'Real?'}),
        }

class Stock_CompanyDepositForm(ModelForm):
    class Meta:
        model = Stock_CompanyDeposit
        fields = { 'stock_comp', 'jpy_deposit', 'usd_deposit'}
        widgets = {
            'stock_comp' : Select(attrs={'class' : 'form-control', 'placeholder' : 'Stock_Company'}),
            'jpy_deposit' : TextInput(attrs={'class' : 'form-control', 'placeholder' : 'JPY_DEPOSIT'}),
            'usd_deposit' : TextInput(attrs={'class' : 'form-control', 'placeholder' : 'USD_DEPOSIT'}),
        }

class StockForm(ModelForm):
    class Meta:
        model = Stock
        fields = { 'name', 'code', 'country'}
        widgets = {
            'name' : TextInput(attrs={'class' : 'form-control', 'placeholder' : 'Stock Name'}),
            'code' : TextInput(attrs={'class' : 'form-control', 'placeholder' : 'Stock Code'}),
            'country' : Select(attrs={'class' : 'form-control', 'placeholder' : 'Country'}),
        }

class StockPriceForm(ModelForm):
    class Meta:
        model = StockPrice
        fields = { 'stock', 'price'}
        widgets = {
            'stock' : Select(attrs={'class' : 'form-control', 'placeholder' : 'Stock'}),
            'price' : TextInput(attrs={'class' : 'form-control', 'placeholder' : 'Stock Price'}),
        }

class H_StockForm(ModelForm):
    class Meta:
        model = H_Stock
        fields = { 'stock', 'stock_company', 'price_ave', 'quantity'}
        widgets = {
            'stock' : Select(attrs={'class' : 'form-control', 'placeholder' : 'Stock Name'}),
            'stock_company' : Select(attrs={'class' : 'form-control', 'placeholder' : 'Stock Company Name'}),
            'price_ave' : TextInput(attrs={'class' : 'form-control', 'placeholder' : 'Stock Average Price'}),
            'quantity' : TextInput(attrs={'class' : 'form-control', 'placeholder' : 'Stock Quantity'}),
        }

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = { 'name', 'password'}
        widgets = {
            'name' : TextInput(attrs={'class' : 'form-control', 'placeholder' : 'UserName'}),
            'password' : TextInput(attrs={'class' : 'form-control', 'placeholder' : 'PASSWORD'}),
        }

class PortfolioForm(ModelForm):
    class Meta:
        model = Portfolio
        fields = { 'name', 'user', 'stock_company', 'h_stock'}
        widgets = {
            'name' : TextInput(attrs={'class' : 'form-control', 'placeholder' : 'Portfolio Name'}),
            'user' : Select(attrs={'class' : 'form-control', 'placeholder' : 'Own User Name'}),
            'stock_company' : Select(attrs={'class' : 'form-control', 'placeholder' : 'Stock Company'}),
            'h_stock' : Select(attrs={'class' : 'form-control', 'placeholder' : 'Holding Stock'}),
        }

class Bank_TradeForm(ModelForm):
    class Meta:
        model = Bank_Trade
        fields = { 'name', 'user', 'inbank', 'outbank', 'currency', 'price', 'fee' }
        widgets = {
            'name' : TextInput(attrs={'class' : 'form-control', 'placeholder' : 'Bank Trade Name'}),
            'user' : Select(attrs={'class' : 'form-control', 'placeholder' : 'Own User Name'}),
            'inbank' : Select(attrs={'class' : 'form-control', 'placeholder' : 'In Bank'}),
            'outbank' : Select(attrs={'class' : 'form-control', 'placeholder' : 'Out Bank'}),
            'currency' : Select(attrs={'class' : 'form-control', 'placeholder' : 'Currency'}),
            'price' : TextInput(attrs={'class' : 'form-control', 'placeholder' : 'Price'}),
            'fee' : TextInput(attrs={'class' : 'form-control', 'placeholder' : 'fee'}),
        }

class Stock_TradeForm(ModelForm):
    class Meta:
        model = Stock_Trade
        fields = { 'name', 'user', 'h_stock', 'trade', 'fee', 'tax' }
        widgets = {
            'name' : TextInput(attrs={'class' : 'form-control', 'placeholder' : 'Stock Trade Name'}),
            'user' : Select(attrs={'class' : 'form-control', 'placeholder' : 'Own User Name'}),
            'h_stock' : Select(attrs={'class' : 'form-control', 'placeholder' : 'Holding Stock'}),
            'trade': Select(attrs={'class' : 'form-control', 'placeholder' : 'Trade'}),
            'fee' : TextInput(attrs={'class' : 'form-control', 'placeholder' : 'fee'}),
            'tax' : TextInput(attrs={'class' : 'form-control', 'placeholder' : 'tax'}),
        }
