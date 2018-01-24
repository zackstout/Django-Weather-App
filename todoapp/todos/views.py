
from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from .models import Todo
from .models import WeatherReal, WeatherPredict
import requests
import datetime
# from django_cron import CronJobBase, Schedule

# from .fusioncharts import FusionCharts

apikey = '24203607faa5b9ea5f063794f983e08d'

def index(request):
    # import matplotlib.pyplot as plt


    from graphos.sources.simple import SimpleDataSource
    from graphos.renderers.gchart import LineChart
    # from graphos.renderers import flot
    # from graphos.renderers.yui import LineChart



    # r = requests.get('https://api.github.com/events')
    # req = r.json()
    result = []
    #Right, dot notation won't work here:
    # for request in req:
    #     result.append(request.actor.avatar_url)

    # r2 = HttpResponse.get('https://api.github.com/events')
    weatherurl = 'http://api.openweathermap.org/data/2.5/forecast?q=%s&APPID=%s' % ('Minneapolis', apikey)
    # weatherurl = 'http://api.openweathermap.org/data/2.5/weather?q=%s&APPID=%s' % ('Minneapolis', apikey)
    # weatherurl = 'http://tile.openweathermap.org/map/%s/%s/%s/%s.png?appid=%s' % ('clouds_new', '1', '22', '33', apikey)

    weather = requests.get(weatherurl)

    weatherList = weather.json()['list']

    for w in weatherList:
        w['dt'] = datetime.datetime.fromtimestamp(
            int(w['dt'])
        ).strftime('%m-%d %H:%M')

    data = [['Date', 'Temp', 'Hum', 'Wind * 5']]

    for index, w in enumerate(weatherList):
        fahr = w['main']['temp'] * 9/5 - 459.67
        wind = w['wind']['speed'] * 5

        #Add to row for chart:
        if (index % 4 == 0):
            predictionFor = w['dt']
            humidity = w['main']['humidity']
            row = [predictionFor, fahr, humidity, wind]
            data.append(row)

        predictionFor = w['dt']
        humidity = w['main']['humidity']
        pressure = w['main']['pressure']
        temp_min = w['main']['temp_min']
        temp_max = w['main']['temp_max']
        description = w['weather'][0]['description']

        # Save to the DB (PredictedWeather table):
        w = WeatherPredict(predictionFor=predictionFor, description=description, temp=fahr, humidity=humidity, windspeed=wind, temp_max=temp_max, temp_min=temp_min, pressure=pressure)
        # w.save()

    chart = LineChart(SimpleDataSource(data=data))

    todos = Todo.objects.all()[:15]

    currentWeather = weatherList[0]
    today = currentWeather['dt']
    fahr = currentWeather['main']['temp'] * 9/5 - 459.67
    wind = currentWeather['wind']['speed'] * 5
    hum = currentWeather['main']['humidity']
    pressure = currentWeather['main']['pressure']
    desc = currentWeather['weather'][0]['description']

    # Save to RealWeather table:
    w = WeatherReal(today=today, humidity=hum, temp=fahr, pressure=pressure, description=desc, windspeed=wind)
    w.save()

    context = {
        'name': 'zack',
        'todos': todos,
        # 'req': req,
        'weather': weatherList,
        'today': weatherList[0],
        'chart': chart,
    }

    return render(request, 'index.html', context)
    # return render(request, 'index.html', { 'output' : column2d.render()})

def details(request, id):
    todo = Todo.objects.get(id=id)
    context = {
        'todo': todo
    }
    return render(request, 'details.html', context)
