from django.urls import path
from . import views

app_name = 'place'
urlpatterns = [
    path('local/<str:areacode>/', views.local, name='local'),
    path('local/<str:areacode>/view/<str:content_id>', views.view, name='view'),
    path('test/', views.test, name='test'),
]
