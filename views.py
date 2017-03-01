from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.utils import timezone

from chartit import DataPool, Chart
from highcharts.views import HighChartsBarView

from .forms import CalendarForm
from .models import Which_Stock, News, Stock_Data

# Create your views here.

# def index(request):
#     return HttpResponse("Welcome to the ftsefinance index page")

def index(request):
    context = dict()
    stocklist = Which_Stock.objects.order_by('-ticker')
    available_stocks = stocklist.exclude(ticker="INDEXFTSE:UKX")
    context['available_stocks']  = available_stocks
    try:
        context['FTSEData'] = stocklist.filter(ticker="INDEXFTSE:UKX")[0]
    except IndexError:
        print("Ftse data not found")

    movers = available_stocks.order_by('-change')
    try:
        context['stock_gainers'] = movers[:5]
    except IndexError:
        if movers > 0:
            context['stock_gainers'] = movers
        print("No Gains")

    try:
        context['stock_lossers'] = movers[len(movers)-5:len(movers)]
    except AssertionError:
        print("No lossers")

    recentnews = News.objects.order_by('-pub_date')
    try:
        context['recentnews'] = recentnews[:5]
    except IndexError:
        context['recentnews'] = ["News not found"]

    # context['pricechart'] = stock_data_plot("INDEXFTSE:UKX")
    # graphtitle = Which_Stock.objects.filter(ticker="INDEXFTSE:UKX")[0]
    # context['graphtitle'] = graphtitle.name
    return render(request, 'ftsefinance/home.html', context)

# def status(request):
#     context = testpage()
#     return render(request, 'main/status.html', context)


def stock_data_plot(q, startdate, step):
    enddate = timezone.now()
    data = q.stock_data_set.filter(date__gt=startdate).order_by('-date')
    close_price = []
    max_price = []
    min_price = []
    for i in range(len(data)):
        # date.append(datetime.strftime(data[i].date, "%d/%m/%Y"))
        close_price.append([int(data[i].date.timestamp()) * 1000,
                            float(data[i].close_price)])
        max_price.append([int(data[i].date.timestamp()) * 1000,
                            float(data[i].max_price)])
        min_price.append([int(data[i].date.timestamp()) * 1000,
                            float(data[i].min_price)])
    data = dict()
    data['close_price'] = close_price
    data['max_price'] = max_price
    data['min_price'] = min_price
    return data

def plot(request, ticker):
    context = dict()
    q = get_object_or_404(Which_Stock, ticker=ticker)
    context['current_stock'] = q
    d, m, y = request.POST.get('start', '0,0,1').split(',')
    print(d,m,y)
    startdate = timezone.now() - relativedelta(days=int(d),
                                                months=int(m),
                                                years=int(y))
    # step = int(request.POST.get('step', '1'))

    context.update(stock_data_plot(q, startdate, step=1))
    #Step 3: Send the chart object to the template.
    return render(request, 'ftsefinance/plot.html', context)

def status(request):
    return HttpResponse("Status page")
