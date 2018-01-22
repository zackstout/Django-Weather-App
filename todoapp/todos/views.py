from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from .models import Todo
import requests

# apikey = '2c35c72f5c9e3ae5e4c914715d470ab1'
apikey = '24203607faa5b9ea5f063794f983e08d'

def index(request):
    r = requests.get('https://api.github.com/events')
    req = r.json()
    result = []
    # for request in req:
    #     result.append(request.actor.avatar_url)

    # r2 = HttpResponse.get('https://api.github.com/events')

    weatherurl = 'http://api.openweathermap.org/data/2.5/forecast?id=524901&APPID=%s' % (apikey)
    weather = requests.get(weatherurl)

    todos = Todo.objects.all()[:10]
    context = {
        'name': 'zack',
        'todos': todos,
        'req': req,
        # 'req': result,
        'weather': weather.json(),

    }
    return render(request, 'index.html', context)

def details(request, id):
    todo = Todo.objects.get(id=id)
    context = {
        'todo': todo
    }
    return render(request, 'details.html', context)
