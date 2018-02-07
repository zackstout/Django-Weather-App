
from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from .models import Todo, WeatherReal, WeatherPredict
# Note: had to pip install schedule
import requests, datetime, schedule, time
from graphos.sources.simple import SimpleDataSource
from graphos.renderers.gchart import LineChart

# note: must re-pip3 install both.
import pandas as pd
from pandas_datareader import data as web

# from .forms import CityForm

from django.template import RequestContext


def get_city(request):
    print('getting city', request)
    # if this is a POST request we need to process the form data
    return 'hi'



apikey = '24203607faa5b9ea5f063794f983e08d'

def getHistory():
    # Nope, need to pay them to get this:
    # now using www1.ncdc.noaa.gov
    histurl = 'http://history.openweathermap.org/data/2.5/history/city?q=Minneapolis,840&type=hour&start=1369728000&end=1369789200'
    hist = requests.get(histurl)

    # print(hist)
    global histList
    histList = hist.json()



def readHistory():
    # Note: had to put csv in penultimate-root folder to get this work.
    # Also had to fix csv: erase some commas among the headers.
    # df = pd.read_csv('weather.csv')

    # Ok cool just use 538 datasets (I forked and cloned their repo of csvs) from now on:
    # They have twitter, weather history, bechdel, college majors, historical ncaa forecasts, love actually crossovers, murder counts by city....

    df = pd.read_csv('tarantino.csv')
    global head
    # df.set_index('TEMP', inplace=True)
    head = df.head(3)
    head = df['movie']

def getWeather(city):
    weatherurl = 'http://api.openweathermap.org/data/2.5/forecast?q=%s&APPID=%s' % (city, apikey)
    # weatherurl = 'http://tile.openweathermap.org/map/%s/%s/%s/%s.png?appid=%s' % ('clouds_new', '1', '22', '33', apikey)

    weather = requests.get(weatherurl)

    global weatherList
    weatherList = weather.json()['list']

    # Subtracting 21600 to try to account for 6 hour difference. It works, but the really weird thing is that our TIMESTAMP is 6 hours ahead! Ok using timezone now instead of datetime.:
    for w in weatherList:
        w['dt'] = datetime.datetime.fromtimestamp(
            int(w['dt'] - 21600)
        ).strftime('%m-%d %H:%M')

    data = [['Date', 'Temp', 'Hum', 'Wind * 5']]

    # Current weather:
    currentWeather = weatherList[0]
    today = currentWeather['dt']
    fahr = currentWeather['main']['temp'] * 9/5 - 459.67
    wind = currentWeather['wind']['speed'] * 5
    hum = currentWeather['main']['humidity']
    pressure = currentWeather['main']['pressure']
    desc = currentWeather['weather'][0]['description']

    # Update RealWeather table for today:

    try:
        p = WeatherReal.objects.get(today=today)
    except WeatherReal.DoesNotExist:
        w = WeatherReal(today=today, humidity=hum, temp=fahr, pressure=pressure, description=desc, windspeed=wind)
        w.save()
    else:
        w = WeatherReal.objects.filter(today=today).update(humidity=hum, temp=fahr, pressure=pressure, description=desc, windspeed=wind)

    # Predicted weather:
    for index, w in enumerate(weatherList[1::]):
        fahr = w['main']['temp'] * 9/5 - 459.67
        wind = w['wind']['speed'] * 5

        # Add to row for chart:
        if (index % 1 == 0):
            predictionFor = w['dt']
            humidity = w['main']['humidity']
            row = [predictionFor, fahr, humidity, wind]
            data.append(row)

        today = weatherList[0]['dt']
        predictionFor = w['dt']
        humidity = w['main']['humidity']
        pressure = w['main']['pressure']
        temp_min = w['main']['temp_min'] * 9/5 - 459.67
        temp_max = w['main']['temp_max'] * 9/5 - 459.67
        description = w['weather'][0]['description']

        # Save to the DB (PredictedWeather table):
        w = WeatherPredict(today=today, predictionFor=predictionFor, description=description, temp=fahr, humidity=humidity, windspeed=wind, temp_max=temp_max, temp_min=temp_min, pressure=pressure)
        w.save()

        # w = WeatherReal(today=predictionFor)
        # w.save()

    global chart
    chart = LineChart(SimpleDataSource(data=data))


def index(request):
    getWeather('Portland')
    readHistory()
    # get_city(request)
    # getHistory()
    # schedule.every(1).minutes.do(getWeather)
    #
    # schedule.every().day.at("02:50").do(getWeather)
    # schedule.every().day.at("05:50").do(getWeather)
    # schedule.every().day.at("08:50").do(getWeather)
    # schedule.every().day.at("11:50").do(getWeather)
    # schedule.every().day.at("14:50").do(getWeather)
    # schedule.every().day.at("17:50").do(getWeather)
    # schedule.every().day.at("20:50").do(getWeather)
    # schedule.every().day.at("23:50").do(getWeather)
    #
    # while True:
    #     schedule.run_pending()
    #     time.sleep(1)

    todos = Todo.objects.all()[:15]

    context = {
        'name': 'zack',
        'todos': todos,
        # 'req': req,
        'weather': weatherList,
        'today': weatherList[0],
        'chart': chart,
        'hist': head,
        # 'all': allReal,
    }

    return render(request, 'index.html', context)

def details(request, id):
    todo = Todo.objects.get(id=id)
    context = {
        'todo': todo
    }
    return render(request, 'details.html', context)
