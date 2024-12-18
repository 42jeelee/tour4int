from django.urls import path
from . import views

app_name = 'place'

urlpatterns = [
    path('local/<str:areacode>/', views.local, name='local'),
    path('local/<str:areacode>/list/', views.local_list, name='local_list'),  
    path('local/<str:areacode>/view/<str:content_id>', views.view, name='view'),
    path('like/<str:content_id>/', views.like_content, name='like'),
    path('comments/<int:place_id>/', views.comment_list, name='comment_list'),
    path('comments/delete/<int:comment_id>/', views.delete_comment, name='delete_comment'),
    path('comments/wirte/', views.wirte_comment, name='wirte_comment'),
    path('comments/modify/<int:comment_id>/', views.modify_comment, name='modify_comment'),
]
