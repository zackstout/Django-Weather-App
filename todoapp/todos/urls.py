from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^cityname/$', views.get_city, name='get_city'),

    url(r'^details/(?P<id>\w{0,50})/$', views.details)
]
