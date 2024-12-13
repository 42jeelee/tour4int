from django.urls import path
from . import views

app_name = 'touradmin'

urlpatterns = [
    path('', views.touradmin, name='index'),
    path('get_place/', views.get_place, name='get_place'),
    path('get_event/', views.get_event, name='get_event'),
    path('get_view/', views.get_view, name='get_view'),
    path('update/', views.update, name='update'),
    path('get_user_view/', views.get_user_view, name='get_user_view'),
    path('upload-image/', views.image_upload, name='upload_image'),
    path('delete-image/', views.delete_image, name='delete_image'),
    path('active_banner/', views.active_banner, name='active_banner'),
    path('deactive_banner/', views.deactive_banner, name='deactive_banner'),
]
