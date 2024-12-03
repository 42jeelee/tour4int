from django.urls import path
from . import views

app_name = 'place'
urlpatterns = [
    path('', views.all, name='all'),
]
