from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from .models import Todo
import requests
import datetime
# from .fusioncharts import FusionCharts


# apikey = '2c35c72f5c9e3ae5e4c914715d470ab1'
apikey = '24203607faa5b9ea5f063794f983e08d'

def index(request):
    # import matplotlib.pyplot as plt

    # data = [
    #     ['a', 'b', 'c'],
    #     [1, 2, 3],
    #     [2, 3, 1],
    #     [3, 4, 4],
    #     [5, 4, 3]
    # ]
    #
    data = [
       ['Year', 'Sales', 'Expenses', 'Items Sold', 'Net Profit'],
       ['2004', 1000, 400, 100, 600],
       ['2005', 1170, 460, 120, 710],
       ['2006', 660, 1120, 50, -460],
       ['2007', 1030, 540, 100, 490],
       ]
    from graphos.sources.simple import SimpleDataSource
    from graphos.renderers.gchart import LineChart
    from graphos.renderers import flot
    # from graphos.renderers.yui import LineChart

    r = requests.get('https://api.github.com/events')
    req = r.json()
    result = []
    # for request in req:
    #     result.append(request.actor.avatar_url)

    # r2 = HttpResponse.get('https://api.github.com/events')

    weatherurl = 'http://api.openweathermap.org/data/2.5/forecast?q=%s&APPID=%s' % ('Minneapolis', apikey)

    # weatherurl = 'http://api.openweathermap.org/data/2.5/weather?q=%s&APPID=%s' % ('Minneapolis', apikey)


    # weatherurl = 'http://tile.openweathermap.org/map/%s/%s/%s/%s.png?appid=%s' % ('clouds_new', '1', '22', '33', apikey)
    weather = requests.get(weatherurl)

    weatherList = weather.json()['list']

    for w in weatherList:
        # result.append(datetime.datetime.fromtimestamp(
        #     int(w['dt'])
        # ).strftime('%Y-%m-%d %H:%M'))
        w['dt'] = datetime.datetime.fromtimestamp(
            int(w['dt'])
        ).strftime('%Y-%m-%d %H:%M')

    data = [['Date', 'Temp', 'Hum']]

    for index, w in enumerate(weatherList):
        fahr = w['main']['temp'] * 9/5 - 459.67
        if (index % 8 == 0):
            row = [w['dt'], fahr, w['main']['humidity']]
            data.append(row)


    # options = {
    #     LineChart.series: {
    #         0: {
    #             targetAxisIndex: 0
    #         },
    #         1: {
    #             targetAxisIndex: 1
    #         }
    #     },
    #     vAxes: {
    #         0: {
    #             title: 'left'
    #         },
    #         1: {
    #             title: 'right'
    #         }
    #     }
    # }

    chart = LineChart(SimpleDataSource(data=data))


    todos = Todo.objects.all()[:10]
    context = {
        'name': 'zack',
        'todos': todos,
        'req': req,
        # 'req': result,
        'weather': weatherList,
        'chart': chart,
        # 'weather': weather
        # 'res': result,

    }

    return render(request, 'index.html', context)
    # return render(request, 'index.html', { 'output' : column2d.render()})

def details(request, id):
    todo = Todo.objects.get(id=id)
    context = {
        'todo': todo
    }
    return render(request, 'details.html', context)
