
from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from .models import Todo, WeatherReal, WeatherPredict
# Note: had to pip install schedule
import requests, datetime, schedule, time
from graphos.sources.simple import SimpleDataSource
from graphos.renderers.gchart import LineChart


apikey = '24203607faa5b9ea5f063794f983e08d'

def getWeather():
    weatherurl = 'http://api.openweathermap.org/data/2.5/forecast?q=%s&APPID=%s' % ('Minneapolis', apikey)
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
        if (index % 4 == 0):
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
    getWeather()
    # schedule.every().day.at("03:00").do(getWeather)
    # schedule.every().day.at("06:00").do(getWeather)
    # schedule.every().day.at("09:00").do(getWeather)
    # schedule.every().day.at("12:00").do(getWeather)
    # schedule.every().day.at("15:00").do(getWeather)
    # schedule.every().day.at("18:00").do(getWeather)
    # schedule.every().day.at("21:00").do(getWeather)
    # schedule.every().day.at("00:00").do(getWeather)

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
        # 'all': allReal,
    }

    return render(request, 'index.html', context)

def details(request, id):
    todo = Todo.objects.get(id=id)
    context = {
        'todo': todo
    }
    return render(request, 'details.html', context)
