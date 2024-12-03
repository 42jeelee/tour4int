from django.urls import path
from . import views

app_name = 'api'
urlpatterns = [
    path('get_place/', views.get_place, name='get_place'),
    path('get_areacode/', views.get_areacode, name='get_areacode'),
]
