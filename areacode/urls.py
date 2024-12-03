from django.urls import path
from . import views

app_name = 'areacode'
urlpatterns = [
    path('', views.all, name='all'),
]
