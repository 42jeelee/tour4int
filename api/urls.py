from django.urls import path
from . import views

app_name = 'api'
urlpatterns = [
    path('get_place/', views.get_place, name='get_place'),
    path('get_pinfo/', views.get_pinfo, name='get_pinfo'),
    path('get_category/', views.get_category, name='get_category'),
    path('get_areacode/', views.get_areacode, name='get_areacode'),
    path('get_event/', views.get_event, name='get_event'),
]
