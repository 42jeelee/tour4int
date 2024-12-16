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
    
    # 회원정보 수정
    path('update-profile/', views.update_profile, name='update_profile'),
    
    # 비밀번호 변경
    path('change-password/', views.change_password, name='change_password'),
    
    # 회원탈퇴
    path('delete/', views.delete_account, name='delete'),
    
    # 이메일 인증 코드 전송 엔드포인트
    path('send-verification-code/', views.send_verification_code, name='send_verification_code'),
    path('verify-email/', views.verify_email, name='verify_email'),
]
