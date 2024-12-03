from django.urls import path
from . import views

app_name = 'localpage'
urlpatterns = [
    path('test/', views.test, name='test'),
]
