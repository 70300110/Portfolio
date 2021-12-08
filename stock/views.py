from django.shortcuts import render, redirect
from .models import Bank, BankDeposit, Stock_Company, Stock_CompanyDeposit, Stock, StockPrice, H_Stock, User, Portfolio, Bank_Trade, Stock_Trade
from django.shortcuts import get_object_or_404
from .forms import BankForm, Stock_CompanyForm, Stock_CompanyDepositForm, StockForm, StockPriceForm, H_StockForm, UserForm, PortfolioForm, Bank_TradeForm, Stock_TradeForm
from django.views.decorators.http import require_POST
from rest_framework.views import APIView
from rest_framework.response import Response

import ccxt
import requests
from bs4 import BeautifulSoup
import os, sys, time, datetime, subprocess, logging, threading
from logging import getLogger, StreamHandler, Formatter, FileHandler
user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.115 Safari/537.36'
header = {
    'User-Agent': user_agent
}

logger = getLogger(__name__)
logger.setLevel(logging.DEBUG)
# flogger = getLogger(__name__)
# flogger.setLevel(logging.DEBUG)
stream_handler = StreamHandler()
stream_handler.setLevel(logging.DEBUG)
# file_handler = FileHandler("C:/Dumps/log/".replace('/', os.sep) + datetime.datetime.now().strftime("%Y%m%d_%H%M%S")[2:] + ".log")
# file_handler = FileHandler(datetime.datetime.now().strftime("%Y%m%d_%H%M%S")[2:] + ".log")
# file_handler.setLevel(logging.DEBUG)
handler_format = Formatter('[ %(asctime)s ] [ %(funcName)s ] [ %(levelname)s ] [%(lineno)s] %(message)s')
stream_handler.setFormatter(handler_format)
# file_handler.setFormatter(handler_format)
logger.addHandler(stream_handler)
# flogger.addHandler(file_handler)

def home(request):
    banks = Bank.objects.all()
    stock_comps = Stock_Company.objects.all()
    stocks = Stock.objects.all()
    h_stocks = H_Stock.objects.all()
    users = User.objects.all()
    portfolios = Portfolio.objects.all()
    return render(request,
                  'accounts/login.html',
                  { 'banks' : banks,
                    'stock_comps' : stock_comps,
                    'stocks' : stocks,
                    'h_stocks' : h_stocks,
                    'users' : users,
                    'portfolios' : portfolios
                  })

bank_list = ('Mistuisumitomo', 'SBI', 'Rakuten', 'Total Bank Deposit', 'Test1', 'Test2')

def dashboard_v1(request):
    banks = Bank.objects.all()
    bdeposits = []
    for bank in banks:
        try:
            bdeposit = BankDeposit.objects.filter(bank__name=bank.name).latest('datetime')
            bdeposits.append(bdeposit)
            print(bdeposit)
        except Exception as e:
            print(e)
        finally:
            print("finally")
        print(bdeposits)
    stock_comps = Stock_Company.objects.all()
    cdeposits = []
    for stock_comp in stock_comps:
        try:
            cdeposit = Stock_CompanyDeposit.objects.filter(stock_comp__id=stock_comp.id).latest('datetime')
            cdeposits.append(cdeposit)
            print(cdeposit)
        except Exception as e:
            print(e)
        finally:
            print("finally")
        print(cdeposits)
    hjstocks = H_Stock.objects.filter(stock__country=1).filter(stock_company__real=1)
    hjstocks = get_top3(hjstocks)
    jsChart = []
    for hjstock in hjstocks:
        jsChart.append({'name':hjstock.stock.name, 'ratio':get_ratio(hjstock)})
    hustocks = H_Stock.objects.filter(stock__country=2).filter(stock_company__real=1)
    hustocks = get_top3(hustocks)
    usChart = []
    for hustock in hustocks:
        usChart.append({'name':hustock.stock.name, 'ratio':get_ratio(hustock)})
    return render(request,
                  'base/dashboard_v1.html',
                  { 'bdeposits' : bdeposits,
                    'cdeposits' : cdeposits,
                    'jsChart' : jsChart,
                    'usChart' : usChart
                  })

def dashboard_v2(request):
    portfolios = Portfolio.objects.all()
    #名前一覧を取得
    pname_list = Portfolio.objects.values_list('name', flat=True)
    # print(list(pname_list))
    # print(set(list(pname_list)))
    pname_list = list(set(list(pname_list)))
    # print(pname_list)
    #取得した名前ごとにポートフォリオを作成
    p = dict(zip(pname_list, pname_list))
    print(p)
    for pname in pname_list:
        plist = Portfolio.objects.filter(name=pname)
        print(plist)
        p[pname] = plist
    # print(p)
    #作成したポートフォリオをごとに必要な情報を計算
    # pinfo = dict(zip(pname_list, pname_list))
    pinfo = []
    for pname in pname_list:
        info2 = []
        for pn in p[pname]:
            # print("{0}\t[{1}]\t{2}\t{3}".format(pn.name, pn.user.name, pn.stock_company.name, pn.h_stock.stock.name))
            #それぞれの株に対して損益・前日比(%)・時価を計算
            info = []
            info.append(get_price_diff(pn.h_stock))
            info.append(get_market_price(pn.h_stock))
            info.append(pn.h_stock.price_ave * pn.h_stock.quantity)
            print("pn : {} \t info : {}".format(pn.name, info))
            info2.append(info)
        print("info2 : {}".format(info2))
        print("-------info2------------")
        price_diff = 0
        market_price = 0
        bought_price = 0
        ratio = 0
        for i in range(len(info2)):
            price_diff += info2[i][0]
            market_price += info2[i][1]
            bought_price += info2[i][2]
        ratio = (market_price - bought_price) / bought_price * 100
        print(pname)
        print("price_diff : {}".format(round(price_diff, 2)))
        print("market_price : {}".format(round(market_price, 2)))
        print("ratio : {}".format(round(ratio, 2)))
        print("\n-------end pname------------\n")
        # pinfo[pname] = {'pname':pname, 'pdiff':price_diff, 'mprice':market_price, 'ratio':ratio }
        pinfo.append({'pname':pname, 'pdiff':round(price_diff, 2), 'mprice':round(market_price, 2), 'ratio':round(ratio, 2) })
        # print("pinfo[{}] = {}".format(pname, pinfo[pname]))

    #表示ようにまとめる
    return render(request,
                  'base/dashboard_v2.html',
                  { 'portfolios' : portfolios,
                    'pname_list' : pname_list,
                    'p' : p,
                    'pinfo' : pinfo
                  })

def dashboard_v3(request):
    binance = ccxt.binance()
    markets = binance.load_markets()
    # pprint(markets)
    params = []
    count = 0
    for ticker in markets:
        if count < 24:
            print(ticker)
            count += 1
            info = binance.fetch_ticker(symbol=ticker)
            print(info)
            cryptocard = {}
            cryptocard['symbol'] = info['symbol']
            cryptocard['datetime'] = info['datetime']
            cryptocard['ask'] = info['ask']
            cryptocard['percentage'] = info['percentage']
            cryptocard['link'] = "https://www.binance.com/ja/trade/" + info['symbol'].replace('/', '_')
            print(cryptocard)
            params.append(cryptocard)

    #表示ようにまとめる
    return render(request,
                  'base/dashboard_v3.html',
                  { 'cryptocard' : params })

def dashboard_v4(request):
    binance = ccxt.binance()
    markets = binance.load_markets()
    # pprint(markets)
    params = []
    inurl = "https://kabureal.net/prompt/"
    response = requests.get(inurl, headers=header)
    soup = BeautifulSoup(response.content,'lxml')

    database = soup.find_all("div", {"class" : "clearfix uline_04 ptop7 pbtm2"})
    for target in database:
        try:
            company  = target.find("div", {"class" : "fs14 a_22 fbold"}).get_text()
            percentage = target.find("span", {"class" : "fs11"}).get_text()
            imageurl = target.find("img")['src']
            link = target.find('a')
            outurl = link.get('href')
            reason = target.find('a', {"class" : "mleft3 fs11"}).get_text()
            # logger.info("{0} : {1} : {2}".format(company, percentage, imageurl))
            # logger.info("{0} : {1} : {2}".format(company, outurl, reason))
            stockinfo = {}
            stockinfo['company'] = company
            stockinfo['percentage'] = float(percentage)
            stockinfo['reason'] = reason
            stockinfo['imageurl'] = imageurl
            stockinfo['outurl'] = outurl
            params.append(stockinfo)
        except:
            logger.debug("Error")

    # pprint(params)

    #表示用にまとめる
    return render(request,
                  'base/dashboard_v4.html',
                  { 'stockinfo' : params })

#-----------URL------------------------------
def index(request):
    banks = Bank.objects.all()
    return render(request, 'base/index.html', { 'banks' : banks })

def index2(request):
    return render(request, 'project/index2.html', {})

def base(request):
    return render(request, 'project/base.html', {})

def detail(request, bank_id):
    bank = get_object_or_404(Bank, id=bank_id)
    return render(request, 'base/detail.html', { 'bank' : bank })

#-----------BANK URL----------------------------------
def table_bank(request):
    deposits = BankDeposit.objects.all()
    return render(request, 'bank/table_bank.html', { 'deposits' : deposits })

def index_bank(request):
    banks = Bank.objects.all()
    deposits = []
    for bank in banks:
        try:
            deposit = BankDeposit.objects.filter(bank__name=bank.name).latest('datetime')
            deposits.append(deposit)
            print(deposit)
        except Exception as e:
            print(e)
        finally:
            print("finally")
        print(deposits)
    return render(request, 'bank/index_bank.html', { 'deposits' : deposits })

def new_bank(request):
    if request.method == "POST":
        form = BankForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('stock:index')
    else:
        form = BankForm
    return render(request, 'bank/new_bank.html', { 'form' : form })

def detail_bank(request, bank_id):
    bank = get_object_or_404(Bank, id=bank_id)
    return render(request, 'bank/detail_bank.html', { 'bank' : bank })

def edit_bank(request, bank_id):
    bank = get_object_or_404(Bank, id=bank_id)
    if request.method == "POST":
        form = BankForm(request.POST, instance=bank)
        if form.is_valid():
            form.save()
            return redirect('stock:index')
    else:
        form = BankForm(instance=bank)
    return render(request, 'bank/edit_bank.html', { 'form':form, 'bank':bank })

# @require_POST
def delete_bank(request, bank_id):
    bank = get_object_or_404(Bank, id=bank_id)
    bank.delete()
    return redirect('stock:index_bank')

#-----------Stock Company URL----------------------------------
def table_stock_comp(request):
    stock_comps = Stock_Company.objects.all()
    return render(request, 'stock_company/table_stock_comp.html', { 'stock_comps' : stock_comps })

def index_stock_comp(request):
    stock_comps = Stock_Company.objects.all()
    deposits = []
    for stock_comp in stock_comps:
        try:
            deposit = Stock_CompanyDeposit.objects.filter(stock_comp__name=stock_comp.name).latest('datetime')
            deposits.append(deposit)
            print(deposit)
        except Exception as e:
            print(e)
        finally:
            print("finally")
        print(deposits)
    return render(request, 'stock_company/index_stock_comp.html', { 'deposits' : deposits })

def new_stock_comp(request):
    if request.method == "POST":
        form = Stock_CompanyForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('stock:index_stock_comp')
    else:
        form = Stock_CompanyForm
    return render(request, 'stock_company/new_stock_comp.html', { 'form' : form })

def detail_stock_comp(request, stock_comp_id):
    stock_comp = get_object_or_404(Stock_Company, id=stock_comp_id)
    return render(request, 'stock_company/detail_stock_comp.html', { 'stock_comp' : stock_comp })

def edit_stock_comp(request, stock_comp_id):
    stock_comp = get_object_or_404(Stock_Company, id=stock_comp_id)
    if request.method == "POST":
        form = Stock_CompanyForm(request.POST, instance=stock_comp)
        if form.is_valid():
            form.save()
            return redirect('stock:index_stock_comp')
    else:
        form = Stock_CompanyForm(instance=stock_comp)
    return render(request, 'stock_company/edit_stock_comp.html', { 'form':form, 'stock_comp':stock_comp })

# @require_POST
def delete_stock_comp(request, deposit_id):
    deposit = get_object_or_404(Stock_CompanyDeposit, id=deposit_id)
    deposit.delete()
    return redirect('stock:index_stock_comp')

#-----------STOCK URL----------------------------------
def table_stock(request):
    stocks = Stock.objects.all()
    return render(request, 'stock/table_stock.html', { 'stocks' : stocks })

def index_stock(request):
    stocks = Stock.objects.all()
    stockprices = []
    for stock in stocks:
        try:
            stockprice = StockPrice.objects.filter(stock__name=stock.name).latest('datetime')
            stockprices.append(stockprice)
            print(stockprice)
        except Exception as e:
            print(e)
        finally:
            print("finally")
        print(stockprices)
    return render(request, 'stock/index_stock.html', { 'stockprices' : stockprices })

def new_stock(request):
    if request.method == "POST":
        form = StockForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('stock:index_stock')
    else:
        form = StockForm
    return render(request, 'stock/new_stock.html', { 'form' : form })

def detail_stock(request, stock_id):
    stock = get_object_or_404(Stock, id=stock_id)
    return render(request, 'stock/detail_stock.html', { 'stock' : stock })

def edit_stock(request, stock_id):
    stock = get_object_or_404(Stock, id=stock_id)
    if request.method == "POST":
        form = StockForm(request.POST, instance=stock)
        if form.is_valid():
            form.save()
            return redirect('stock:index_stock')
    else:
        form = StockForm(instance=stock)
    return render(request, 'stock/edit_stock.html', { 'form':form, 'stock':stock })

# @require_POST
def delete_stock(request, stock_id):
    stock = get_object_or_404(Stock, id=stock_id)
    stock.delete()
    return redirect('stock:index_stock')

#-----------Holding STOCK URL----------------------------------
def table_h_stock(request):
    h_stocks = H_Stock.objects.all()
    return render(request, 'h_stock/table_h_stock.html', { 'h_stocks' : h_stocks })

def index_h_stock(request):
    h_stocks = H_Stock.objects.all()
    return render(request, 'h_stock/index_h_stock.html', { 'h_stocks' : h_stocks })

def new_h_stock(request):
    if request.method == "POST":
        form = H_StockForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('stock:index_h_stock')
    else:
        form = H_StockForm
    return render(request, 'h_stock/new_h_stock.html', { 'form' : form })

def detail_h_stock(request, h_stock_id):
    h_stock = get_object_or_404(H_Stock, id=h_stock_id)
    return render(request, 'h_stock/detail_h_stock.html', { 'h_stock' : h_stock })

def edit_h_stock(request, h_stock_id):
    h_stock = get_object_or_404(h_Stock, id=h_stock_id)
    if request.method == "POST":
        form = H_StockForm(request.POST, instance=h_stock)
        if form.is_valid():
            form.save()
            return redirect('stock:index_h_stock')
    else:
        form = H_StockForm(instance=h_stock)
    return render(request, 'h_stock/edit_h_stock.html', { 'form':form, 'h_stock':h_stock })

# @require_POST
def delete_h_stock(request, h_stock_id):
    h_stock = get_object_or_404(H_Stock, id=h_stock_id)
    h_stock.delete()
    return redirect('stock:index_h_stock')

#-----------UESR URL----------------------------------
def table_user(request):
    users = User.objects.all()
    return render(request, 'user/table_user.html', { 'users' : users })

def index_user(request):
    users = User.objects.all()
    return render(request, 'user/index_user.html', { 'users' : users })

def new_user(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('stock:index_user')
    else:
        form = UserForm
    return render(request, 'user/new_user.html', { 'form' : form })

def detail_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    return render(request, 'user/detail_user.html', { 'user' : user })

def edit_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == "POST":
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('stock:index_user')
    else:
        form = UserForm(instance=user)
    return render(request, 'user/edit_user.html', { 'form':form, 'user':user })

# @require_POST
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.delete()
    return redirect('stock:index_user')

#-----------PORTFOLIO URL----------------------------------
def table_portfolio(request):
    portfolios = Portfolio.objects.all()
    return render(request, 'portfolio/table_portfolio.html', { 'portfolios' : portfolios })

def index_portfolio(request):
    portfolios = Portfolio.objects.all()
    return render(request, 'portfolio/index_portfolio.html', { 'portfolios' : portfolios })

def new_portfolio(request):
    if request.method == "POST":
        form = PortfolioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('stock:index_portfolio')
    else:
        form = PortfolioForm
    return render(request, 'portfolio/new_portfolio.html', { 'form' : form })

def detail_portfolio(request, portfolio_id):
    portfolio = get_object_or_404(Portfolio, id=portfolio_id)
    return render(request, 'portfolio/detail_portfolio.html', { 'portfolio' : portfolio })

def edit_portfolio(request, portfolio_id):
    portfolio = get_object_or_404(Portfolio, id=portfolio_id)
    if request.method == "POST":
        form = PortfolioForm(request.POST, instance=portfolio)
        if form.is_valid():
            form.save()
            return redirect('stock:index_portfolio')
    else:
        form = PortfolioForm(instance=portfolio)
    return render(request, 'portfolio/edit_portfolio.html', { 'form':form, 'portfolio':portfolio })

# @require_POST
def delete_portfolio(request, portfolio_id):
    portfolio = get_object_or_404(Portfolio, id=portfolio_id)
    portfolio.delete()
    return redirect('stock:index_portfolio')

#-----------Bank Trade URL----------------------------------
def table_bank_trade(request):
    bank_trades = Bank_Trade.objects.all()
    return render(request, 'bank_trade/table_bank_trade.html', { 'bank_trades' : bank_trades })

def index_bank_trade(request):
    bank_trades = Bank_Trade.objects.all()
    return render(request, 'bank_trade/index_bank_trade.html', { 'bank_trades' : bank_trades })

def new_bank_trade(request):
    if request.method == "POST":
        form = Bank_TradeForm(request.POST)
        if form.is_valid():
            print("")
            inbank = Bank.objects.filter(id=request.POST['inbank']).latest('datetime')
            print("IN Bank: " + str(inbank.id) + ' ' + inbank.name)
            outbank = Bank.objects.filter(id=request.POST['outbank']).latest('datetime')
            print("OUT Bank: " + str(outbank.id) + ' ' + outbank.name)
            indeposit = BankDeposit.objects.filter(bank=inbank).latest('datetime')
            print(str(indeposit.id) + ' ' + indeposit.bank.name + ' ' + str(indeposit.jpy_deposit))
            outdeposit = BankDeposit.objects.filter(bank=outbank).latest('datetime')
            print(str(outdeposit.id) + ' ' + outdeposit.bank.name + ' ' + str(outdeposit.jpy_deposit))
            price = request.POST['price']
            fee = request.POST['fee']
            if request.POST['currency'] == '1':
                afterindeposit = indeposit.jpy_deposit + float(price)
                afteroutdeposit = outdeposit.jpy_deposit - (float(price) + float(fee))
                print("price: " + str(price) + "\t fee: " + str(fee))
                print("IN Bank Deposit: " + str(indeposit.jpy_deposit) + " + " + str(price) + " = " + str(afterindeposit))
                print("OUT Bank Deposit: " + str(outdeposit.jpy_deposit) + " - " + str(price) + " - " + str(fee) + " = " + str(afteroutdeposit))
                inbd = BankDeposit(bank=inbank, jpy_deposit=afterindeposit, usd_deposit=indeposit.usd_deposit)
                outbd = BankDeposit(bank=outbank, jpy_deposit=afteroutdeposit, usd_deposit=outdeposit.usd_deposit)
            elif request.POST['currency'] == '2':
                afterindeposit = indeposit.usd_deposit + float(price)
                afteroutdeposit = outdeposit.usd_deposit - (float(price) + float(fee))
                inbd = BankDeposit(bank=inbank, jpy_deposit=indeposit.usd_deposit, usd_deposit=afterindeposit)
                outbd = BankDeposit(bank=outbank, jpy_deposit=outdeposit.usd_deposit, usd_deposit=afteroutdeposit)
            print("")
            form.save()
            inbd.save()
            outbd.save()
            return redirect('stock:index_bank_trade')
    else:
        form = Bank_TradeForm
    return render(request, 'bank_trade/new_bank_trade.html', { 'form' : form })

def detail_bank_trade(request, bank_trade_id):
    bank_trade = get_object_or_404(Bank_Trade, id=bank_trade_id)
    return render(request, 'bank_trade/detail_bank_trade.html', { 'bank_trade' : bank_trade })

def edit_bank_trade(request, bank_trade_id):
    bank_trade = get_object_or_404(Bank_Trade, id=bank_trade_id)
    if request.method == "POST":
        form = Bank_TradeForm(request.POST, instance=bank_trade)
        if form.is_valid():
            form.save()
            return redirect('stock:index_bank_trade')
    else:
        form = Bank_TradeForm(instance=bank_trade)
    return render(request, 'bank_trade/edit_bank_trade.html', { 'form':form, 'bank_trade':bank_trade })

# @require_POST
def delete_bank_trade(request, bank_trade_id):
    bank_trade = get_object_or_404(Bank_Trade, id=bank_trade_id)
    bank_trade.delete()
    return redirect('stock:index_bank_trade')

#-----------Stock Trade URL----------------------------------
def table_stock_trade(request):
    stock_trades = Stock_Trade.objects.all()
    return render(request, 'stock_trade/table_stock_trade.html', { 'stock_trades' : stock_trades })

def index_stock_trade(request):
    stock_trades = Stock_Trade.objects.all()
    return render(request, 'stock_trade/index_stock_trade.html', { 'stock_trades' : stock_trades })

def new_stock_trade(request):
    if request.method == "POST":
        form = {'stock' : request.POST['stock'], 'stock_company' : request.POST['stock_company'], 'price_ave': request.POST['price_ave'], 'quantity' : request.POST['quantity']}
        print(form)
        form1 = H_StockForm(form)
        h_stock = H_Stock.objects.filter(stock=request.POST['stock']).latest('datetime')
        print(h_stock.id)
        form = {'name' : request.POST['name'], 'user' : request.POST['user'], 'h_stock' : h_stock.id, 'trade' : request.POST['trade'], 'fee' : request.POST['fee'], 'tax' : request.POST['tax']}
        print(form)
        form2 = Stock_TradeForm(form)
        print("")
        if form1.is_valid() & form2.is_valid():
            print("")
            stock_company = Stock_Company.objects.filter(id=request.POST['stock_company']).latest('datetime')
            print("Stock_Company: " + str(stock_company.id) + ' ' + stock_company.name + "[" + stock_company.account + "]")
            deposit = Stock_CompanyDeposit.objects.filter(stock_comp=stock_company).latest('datetime')
            print(str(deposit.id) + ' ' + deposit.stock_comp.name + ' ' + str(deposit.jpy_deposit))
            price_ave = request.POST['price_ave']
            quantity = request.POST['quantity']
            fee = request.POST['fee']
            tax = request.POST['tax']
            if request.POST['trade'] == '1':
                if h_stock.stock.country == 1:
                    afterindeposit = deposit.jpy_deposit - float(fee) - float(tax) - (float(price_ave) * float(quantity))
                    print("fee: " + str(fee) + "\t tax: " + str(tax))
                    print("Deposit: " + str(deposit.jpy_deposit) + " - " + str(fee) + "-" + str(tax) + "-" + str(price_ave) + "*" + str(quantity) + "=" + str(afterindeposit))
                    scd = Stock_CompanyDeposit(stock_comp=stock_company, jpy_deposit=afterindeposit, usd_deposit=deposit.usd_deposit)
                elif h_stock.stock.country == 2:
                    afterindeposit = deposit.usd_deposit - float(fee) - float(tax) - (float(price_ave) * float(quantity))
                    print("fee: " + str(fee) + "\t tax: " + str(tax))
                    print("Deposit: " + str(deposit.usd_deposit) + " - " + str(fee) + "-" + str(tax) + "-" + str(price_ave) + "*" + str(quantity) + "=" + str(afterindeposit))
                    scd = Stock_CompanyDeposit(stock_comp=stock_company, jpy_deposit=deposit.jpy_deposit, usd_deposit=deposit.afterindeposit)
                else:
                    print("Which Country?")
                    return redirect('stock:index_stock_trade')
            elif request.POST['trade'] == '2':
                if h_stock.stock.country == 1:
                    afterindeposit = deposit.jpy_deposit - float(fee) - float(tax) + (float(price_ave) * float(quantity))
                    print("fee: " + str(fee) + "\t tax: " + str(tax))
                    print("Deposit: " + str(deposit.jpy_deposit) + " - " + str(fee) + "-" + str(tax) + "+" + str(price_ave) + "*" + str(quantity) + "=" + str(afterindeposit))
                    scd = Stock_CompanyDeposit(stock_comp=stock_company, jpy_deposit=afterindeposit, usd_deposit=deposit.usd_deposit)
                elif h_stock.stock.country == 2:
                    afterindeposit = deposit.usd_deposit - float(fee) - float(tax) + (float(price_ave) * float(quantity))
                    print("fee: " + str(fee) + "\t tax: " + str(tax))
                    print("Deposit: " + str(deposit.usd_deposit) + " - " + str(fee) + "-" + str(tax) + "+" + str(price_ave) + "*" + str(quantity) + "=" + str(afterindeposit))
                    scd = Stock_CompanyDeposit(stock_comp=stock_company, jpy_deposit=deposit.jpy_deposit, usd_deposit=deposit.afterindeposit)
                else:
                    print("Which Country?")
                    return redirect('stock:index_stock_trade')
            print("")
            form1.save()
            form2.save()
            scd.save()
            return redirect('stock:index_stock_trade')
    else:
        form = Stock_TradeForm
        form2 = H_StockForm
    return render(request, 'stock_trade/new_stock_trade.html', { 'form' : form, 'form2' : form2 })

def detail_stock_trade(request, stock_trade_id):
    stock_trade = get_object_or_404(Stock_Trade, id=stock_trade_id)
    return render(request, 'stock_trade/detail_stock_trade.html', { 'stock_trade' : stock_trade })

def edit_stock_trade(request, stock_trade_id):
    stock_trade = get_object_or_404(Stock_Trade, id=stock_trade_id)
    if request.method == "POST":
        form = Stock_TradeForm(request.POST, instance=stock_trade)
        if form.is_valid():
            form.save()
            return redirect('stock:index_stock_trade')
    else:
        form = Stock_TradeForm(instance=stock_trade)
    return render(request, 'stock_trade/edit_stock_trade.html', { 'form':form, 'stock_trade':stock_trade })

# @require_POST
def delete_stock_trade(request, stock_trade_id):
    stock_trade = get_object_or_404(Stock_Trade, id=stock_trade_id)
    stock_trade.delete()
    return redirect('stock:index_stock_trade')

# -------JSON Response------------------------
class ChartData(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        labels = ['Red', 'Blue', 'Yellow', 'Green', 'Purple', 'Orange']
        default_items =  [12, 19, 3, 5, 2, 3]
        data = {
            "labels" : labels,
            "default" : default_items,
        }
        return Response(data)

class InvestRatioChart(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        jpy = 0
        usd = 0
        # get cash total ammount
        bdeposits = []
        cdeposits = []
        banks = Bank.objects.filter(real=1)
        for bank in banks:
            deposit = BankDeposit.objects.filter(bank=bank).latest('datetime')
            bdeposits.append(deposit)
            jpy += deposit.jpy_deposit
            usd += deposit.usd_deposit
        comps = Stock_Company.objects.filter(real=1)
        for comp in comps:
            deposit = Stock_CompanyDeposit.objects.filter(stock_comp=comp).latest('datetime')
            jpy += deposit.jpy_deposit
            usd += deposit.usd_deposit
            cdeposits.append(deposit)
        jpy = jpy +  (usd * 107)
        # get japan investment total ammount
        hjsdeposit = 0
        try:
            hstocks = H_Stock.objects.filter(stock__country=1)
        except Exception as e:
            pass
        for hstock in hstocks:
            hjsdeposit += hstock.price_ave * hstock.quantity
        # get usa investment total ammount
        husdeposit = 0
        hstocks = H_Stock.objects.filter(stock__country=2)
        for hstock in hstocks:
            husdeposit += hstock.price_ave * hstock.quantity
        husdeposit = husdeposit * 107
        default_items =  [jpy, hjsdeposit, husdeposit]
        data = {
            "default" : default_items,
        }
        return Response(data)

def multi(hjsd):
    return (hjsd.price_ave * hjsd.quantity)

def get_top3(stocks):
    sorted(stocks, key=multi)
    print(stocks[:3])
    return stocks[:3]

def get_price_diff(hstock):
    nprice = StockPrice.objects.filter(stock=hstock.stock).latest('datetime')
    return (nprice.price - hstock.price_ave)

def get_ratio(hstock):
    nprice = StockPrice.objects.filter(stock=hstock.stock).latest('datetime')
    ans = (nprice.price - hstock.price_ave) / hstock.price_ave * 100
    # print(round(ans, 2))
    return round(ans, 2)

def get_market_price(hstock):
    nprice = StockPrice.objects.filter(stock=hstock.stock).latest('datetime')
    return nprice.price * hstock.quantity
