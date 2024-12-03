from django.urls import path
from . import views

app_name = 'category'
urlpatterns = [
    path('all/', views.all, name='all'),
    path('test/', views.test, name='test'),
]
