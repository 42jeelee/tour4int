from django.urls import path
from . import views

app_name = 'api'
urlpatterns = [
    path('init_all/', views.init_all, name='init_all'),
    path('init_place/', views.init_place, name='init_place'),
    path('init_category/', views.init_category, name='init_category'),
    path('init_areacode/', views.init_areacode, name='init_areacode'),
    path('init_sigungucode/', views.init_sigungucode, name='init_sigungucode'),
    path('get_event/', views.get_event, name='get_event'),
]
