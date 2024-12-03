from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import SignUpForm, LoginForm, UserUpdateForm, CustomPasswordChangeForm
from .models import User

# Create your views here.

def signup_view(request):
    """
    회원가입 뷰 - 새로운 사용자 등록
    """
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, '회원가입이 성공적으로 완료되었습니다!')
            return redirect('index')
    else:
        form = SignUpForm()
    
    return render(request, 'accounts/signup.html', {'form': form})

def login_view(request):
    """
    로그인 뷰 - 사용자 인증
    """
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, '로그인 성공!')
            return redirect('index')
    else:
        form = LoginForm()
    
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    """
    로그아웃 뷰
    """
    logout(request)
    messages.success(request, '로그아웃 되었습니다.')
    return redirect('index')

@login_required
def mypage_view(request):
    """
    마이페이지 뷰 - 사용자 정보 확인 및 수정
    """
    try:
        user_info = request.user.user_info
    except User.DoesNotExist:
        user_info = User.objects.create(
            user_id=request.user,
            name='',
            nickname='',
            address=''
        )

    if request.method == 'POST':
        # 프로필 수정 폼이 제출된 경우
        if 'profile_submit' in request.POST:
            profile_form = UserUpdateForm(request.POST, instance=user_info)
            if profile_form.is_valid():
                user_info = profile_form.save()
                messages.success(request, '프로필이 성공적으로 업데이트되었습니다.')
                return redirect('accounts:mypage')
            password_form = CustomPasswordChangeForm(request.user)
        
        # 비밀번호 변경 폼이 제출된 경우
        elif 'password_submit' in request.POST:
            password_form = CustomPasswordChangeForm(request.user, request.POST)
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)
                messages.success(request, '비밀번호가 성공적으로 변경되었습니다.')
                return redirect('accounts:mypage')
            profile_form = UserUpdateForm(instance=user_info)
    else:
        profile_form = UserUpdateForm(instance=user_info)
        password_form = CustomPasswordChangeForm(request.user)
    
    return render(request, 'accounts/mypage.html', {
        'profile_form': profile_form,
        'password_form': password_form
    })
