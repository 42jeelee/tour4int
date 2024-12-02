from django.urls import path
from . import views

# URL 네임스페이스 설정
app_name = 'accounts'

urlpatterns = [
    # 회원가입 페이지
    path('signup/', views.signup_view, name='signup'),
    
    # 로그인 페이지
    path('login/', views.login_view, name='login'),
    
    # 로그아웃
    path('logout/', views.logout_view, name='logout'),
    
    # 마이페이지
    path('my/', views.mypage_view, name='mypage'),
]
