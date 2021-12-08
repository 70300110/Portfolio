from django.urls import path
from . import views
from .views import ChartData, InvestRatioChart

app_name = 'stock'
urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard_v1', views.dashboard_v1, name='dashboard_v1'),
    path('dashboard_v2', views.dashboard_v2, name='dashboard_v2'),
    path('dashboard_v3', views.dashboard_v3, name='dashboard_v3'),
    path('dashboard_v4', views.dashboard_v4, name='dashboard_v4'),
    # --------------URL---------------------------------
    path('index', views.index, name='index'),
    path('index2', views.index2, name='index2'),
    path('base', views.base, name='base'),
    path('<int:id>', views.detail, name='detail'),
    # --------------BANK URL---------------------------------
    path('index_bank', views.index_bank, name='index_bank'),
    path('table_bank', views.table_bank, name='table_bank'),
    path('new_bank', views.new_bank, name='new_bank'),
    path('detail_bank/<int:bank_id>', views.detail_bank, name='detail_bank'),
    path('edit_bank/<int:bank_id>', views.edit_bank, name='edit_bank'),
    path('delete_bank/<int:bank_id>', views.delete_bank, name='delete_bank'),
    # --------------Stock Company-------------------------------
    path('index_stock_comp', views.index_stock_comp, name='index_stock_comp'),
    path('table_stock_comp', views.table_stock_comp, name='table_stock_comp'),
    path('new_stock_comp', views.new_stock_comp, name='new_stock_comp'),
    path('detail_stock_comp/<int:stock_comp_id>', views.detail_stock_comp, name='detail_stock_comp'),
    path('edit_stock_comp/<int:stock_comp_id>', views.edit_stock_comp, name='edit_stock_comp'),
    path('delete_stock_comp/<int:stock_comp_id>', views.delete_stock_comp, name='delete_stock_comp'),
    # --------------STOCK URL---------------------------------
    path('index_stock', views.index_stock, name='index_stock'),
    path('table_stock', views.table_stock, name='table_stock'),
    path('new_stock', views.new_stock, name='new_stock'),
    path('detail_stock/<int:stock_id>', views.detail_stock, name='detail_stock'),
    path('edit_stock/<int:stock_id>', views.edit_stock, name='edit_stock'),
    path('delete_stock/<int:stock_id>', views.delete_stock, name='delete_stock'),
    # ---------Holding STOCK URL---------------------------------
    path('index_h_stock', views.index_h_stock, name='index_h_stock'),
    path('table_h_stock', views.table_h_stock, name='table_h_stock'),
    path('new_h_stock', views.new_h_stock, name='new_h_stock'),
    path('detail_h_stock/<int:h_stock_id>', views.detail_h_stock, name='detail_h_stock'),
    path('edit_h_stock/<int:h_stock_id>', views.edit_h_stock, name='edit_h_stock'),
    path('delete_h_stock/<int:h_stock_id>', views.delete_h_stock, name='delete_h_stock'),
    # --------------USER URL---------------------------------
    path('index_user', views.index_user, name='index_user'),
    path('table_user', views.table_user, name='table_user'),
    path('new_user', views.new_user, name='new_user'),
    path('detail_user/<int:user_id>', views.detail_user, name='detail_user'),
    path('edit_user/<int:user_id>', views.edit_user, name='edit_user'),
    path('delete_user/<int:user_id>', views.delete_user, name='delete_user'),
    # --------------bank_trade URL---------------------------------
    path('index_portfolio', views.index_portfolio, name='index_portfolio'),
    path('table_portfolio', views.table_portfolio, name='table_portfolio'),
    path('new_portfolio', views.new_portfolio, name='new_portfolio'),
    path('detail_portfolio/<int:portfolio_id>', views.detail_portfolio, name='detail_portfolio'),
    path('edit_portfolio/<int:portfolio_id>', views.edit_portfolio, name='edit_portfolio'),
    path('delete_portfolio/<int:portfolio_id>', views.delete_portfolio, name='delete_portfolio'),
    # --------------Bank Trade URL---------------------------------
    path('index_bank_trade', views.index_bank_trade, name='index_bank_trade'),
    path('table_bank_trade', views.table_bank_trade, name='table_bank_trade'),
    path('new_bank_trade', views.new_bank_trade, name='new_bank_trade'),
    path('detail_bank_trade/<int:bank_trade_id>', views.detail_bank_trade, name='detail_bank_trade'),
    path('edit_bank_trade/<int:bank_trade_id>', views.edit_bank_trade, name='edit_bank_trade'),
    path('delete_bank_trade/<int:bank_trade_id>', views.delete_bank_trade, name='delete_bank_trade'),
    # --------------Stock Trade URL---------------------------------
    path('index_stock_trade', views.index_stock_trade, name='index_stock_trade'),
    path('table_stock_trade', views.table_stock_trade, name='table_stock_trade'),
    path('new_stock_trade', views.new_stock_trade, name='new_stock_trade'),
    path('detail_stock_trade/<int:stock_trade_id>', views.detail_stock_trade, name='detail_stock_trade'),
    path('edit_stock_trade/<int:stock_trade_id>', views.edit_stock_trade, name='edit_stock_trade'),
    path('delete_stock_trade/<int:stock_trade_id>', views.delete_stock_trade, name='delete_stock_trade'),
    # --------------JSON Response------------------------------------
    path('api/chart/data', ChartData.as_view()),
    path('api/chart/iratio', InvestRatioChart.as_view()),
]
