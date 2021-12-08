from django.contrib import admin
from .models import Bank, BankDeposit, Stock_Company, Stock_CompanyDeposit, Stock, StockPrice, H_Stock, User, Portfolio, Bank_Trade, Stock_Trade

class BankAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'real', 'datetime')
    list_display_links = ('id', 'name', 'real')

class BankDepositAdmin(admin.ModelAdmin):
    list_display = ('id', 'bank', 'jpy_deposit', 'usd_deposit', 'datetime')
    list_display_links = ('id', 'bank', 'jpy_deposit', 'usd_deposit')

class Stock_CompanyAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'account', 'real', 'datetime')
    list_display_links = ('id', 'name', 'account', 'real')

class Stock_CompanyDepositAdmin(admin.ModelAdmin):
    list_display = ('id', 'stock_comp', 'jpy_deposit', 'usd_deposit', 'datetime')
    list_display_links = ('id', 'stock_comp', 'jpy_deposit', 'usd_deposit')

class StockAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'code', 'country', 'datetime')
    list_display_links = ('id', 'name', 'code', 'country')

class StockPriceAdmin(admin.ModelAdmin):
    list_display = ('id', 'stock', 'price', 'datetime')
    list_display_links = ('id', 'stock', 'price')

class H_StockAdmin(admin.ModelAdmin):
    list_display = ('id', 'stock', 'stock_company', 'price_ave', 'quantity', 'datetime')
    list_display_links = ('id', 'stock', 'stock_company', 'price_ave', 'quantity')

class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'password')
    list_display_links = ('id', 'name', 'password')

class PortfolioAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'user', 'stock_company', 'h_stock', 'datetime')
    list_display_links = ('id', 'name', 'user', 'stock_company', 'h_stock')

class Bank_TradeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'user', 'inbank', 'outbank', 'currency', 'price', 'fee', 'datetime')
    list_display_links = ('id', 'name', 'user', 'inbank', 'outbank', 'currency','price', 'fee')

class Stock_TradeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'user', 'h_stock', 'trade', 'fee', 'tax', 'datetime')
    list_display_links = ('id', 'name', 'user', 'h_stock', 'trade', 'fee', 'tax')

admin.site.register(Bank, BankAdmin)
admin.site.register(BankDeposit, BankDepositAdmin)
admin.site.register(Stock_Company, Stock_CompanyAdmin)
admin.site.register(Stock_CompanyDeposit, Stock_CompanyDepositAdmin)
admin.site.register(Stock, StockAdmin)
admin.site.register(StockPrice, StockPriceAdmin)
admin.site.register(H_Stock, H_StockAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Portfolio, PortfolioAdmin)
admin.site.register(Bank_Trade, Bank_TradeAdmin)
admin.site.register(Stock_Trade, Stock_TradeAdmin)
