from django.urls import path
from . import views

app_name = 'touradmin'
urlpatterns = [
    path('', views.index, name='index'),
]
