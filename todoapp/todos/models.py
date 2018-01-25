from django.db import models
from datetime import datetime

# Create your models here.
class Todo(models.Model):
    title = models.CharField(max_length=200)
    test = models.TextField()
    created_at = models.DateTimeField(default=datetime.now, blank=True)

class WeatherReal(models.Model):
    timestamp = models.DateTimeField(default=datetime.now, blank=True)
    today = models.CharField(default='', max_length=50)
    temp = models.IntegerField(default=0)
    humidity = models.IntegerField(default=0)
    description = models.CharField(default='', max_length=50)
    windspeed = models.IntegerField(default=0)
    pressure = models.IntegerField(default=0)

    def __str__(self):
        return self.today

class WeatherPredict(models.Model):
    timestamp = models.DateTimeField(default=datetime.now, blank=True)
    today = models.CharField(default='', max_length=50)
    temp = models.IntegerField(default=0)
    humidity = models.IntegerField(default=0)
    description = models.CharField(default='', max_length=50)
    windspeed = models.IntegerField(default=0)
    pressure = models.IntegerField(default=0)
    temp_max = models.IntegerField(default=0)
    temp_min = models.IntegerField(default=0)
    predictionFor = models.CharField(default='', max_length=50)

    def __str__(self):
        return self.predictionFor

def __str__(self):
    return self.title
