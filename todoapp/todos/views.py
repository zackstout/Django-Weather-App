from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from .models import Todo

def index(request):
    todos = Todo.objects.all()[:10]
    context = {
    'name': 'zack',
    'todos': todos
    }
    return render(request, 'index.html', context)
