from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import SignUpForm, LoginForm, UserUpdateForm, CustomPasswordChangeForm
from .models import User

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
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(username=email, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, '로그인 성공!')
                return redirect('index')
            else:
                messages.error(request, '아이디 또는 비밀번호가 올바르지 않습니다.')
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
    마이페이지 뷰 - 사용자 정보 조회 및 수정
    """
    if request.method == 'POST':
        if 'profile_submit' in request.POST:
            profile_form = UserUpdateForm(request.POST, instance=request.user)
            if profile_form.is_valid():
                profile_form.save()
                messages.success(request, '회원정보가 성공적으로 수정되었습니다.')
                return redirect('accounts:mypage')
            password_form = CustomPasswordChangeForm(request.user)
        elif 'password_submit' in request.POST:
            password_form = CustomPasswordChangeForm(request.user, request.POST)
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)  # 세션 유지
                messages.success(request, '비밀번호가 성공적으로 변경되었습니다.')
                return redirect('accounts:mypage')
            profile_form = UserUpdateForm(instance=request.user)
    else:
        profile_form = UserUpdateForm(instance=request.user)
        password_form = CustomPasswordChangeForm(request.user)
    
    return render(request, 'accounts/mypage.html', {
        'profile_form': profile_form,
        'password_form': password_form,
        'user': request.user
    })
