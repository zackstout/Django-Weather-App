from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from .models import Todo
import requests
import datetime

# apikey = '2c35c72f5c9e3ae5e4c914715d470ab1'
apikey = '24203607faa5b9ea5f063794f983e08d'

def index(request):
    import matplotlib.pyplot as plt

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


    todos = Todo.objects.all()[:10]
    context = {
        'name': 'zack',
        'todos': todos,
        'req': req,
        # 'req': result,
        'weather': weatherList,
        # 'weather': weather
        # 'res': result,

    }
    return render(request, 'index.html', context)

def details(request, id):
    todo = Todo.objects.get(id=id)
    context = {
        'todo': todo
    }
    return render(request, 'details.html', context)
