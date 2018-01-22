from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from .models import Todo
import requests

def index(request):
    r = requests.get('https://api.github.com/events')
    todos = Todo.objects.all()[:10]
    context = {
        'name': 'zack',
        'todos': todos,
        'req': r.json(),

    }
    return render(request, 'index.html', context)

def details(request, id):
    todo = Todo.objects.get(id=id)
    context = {
        'todo': todo
    }
    return render(request, 'details.html', context)
