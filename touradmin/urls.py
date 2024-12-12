from django.urls import path
from . import views

app_name = 'touradmin'
urlpatterns = [
    path('', views.touradmin, name='index'),
    path('get_place/', views.get_place, name='get_place'),
    path('get_event/', views.get_event, name='get_event'),
    path('get_view/', views.get_view, name='get_view'),
    path('update/', views.update, name='update'),
]
