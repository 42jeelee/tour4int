from django.urls import path
from . import views

app_name = 'place'

urlpatterns = [
    path('local/<str:areacode>/', views.local, name='local'),
    path('test/', views.test, name='test'),
]
