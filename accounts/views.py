from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.http import JsonResponse
from .forms import SignUpForm, LoginForm, UserUpdateForm, CustomPasswordChangeForm
from .models import User, EmailVerification
from .utils import send_verification_email
from django.conf import settings

def signup_view(request):
    """
    회원가입 뷰 - 새로운 사용자 등록
    """
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.is_email_verified = True
            user.save()
            login(request, user)
            messages.success(request, '환영합니다! 회원가입이 완료되었습니다. 즐거운 여행 되세요!')
            return redirect('index')
    else:
        form = SignUpForm()
    
    return render(request, 'accounts/signup.html', {'form': form})

def send_verification_code(request):
    """
    이메일 인증 코드 전송
    """
    if request.method == 'POST':
        email = request.POST.get('email')
        if email:
            try:
                # 인증 코드 생성 및 저장
                verification = EmailVerification.create_verification(email)
                # 이메일 전송
                send_verification_email(email, verification.verification_code)
                return JsonResponse({
                    'success': True,
                    'message': '인증 코드가 이메일로 전송되었습니다.'
                })
            except Exception as e:
                # 개발 환경에서만 상세 오류 메시지 표시
                if settings.DEBUG:
                    error_message = f'이메일 전송 실패: {str(e)}'
                else:
                    error_message = '이메일 전송에 실패했습니다. 다시 시도해주세요.'
                
                return JsonResponse({
                    'success': False,
                    'message': error_message
                })
    return JsonResponse({
        'success': False,
        'message': '잘못된 요청입니다.'
    })

def verify_email(request):
    """
    이메일 인증 코드 확인
    """
    if request.method == 'POST':
        email = request.POST.get('email')
        code = request.POST.get('verification_code')
        
        try:
            verification = EmailVerification.objects.get(
                email=email,
                verification_code=code,
                is_verified=False,
                expires_at__gt=timezone.now()
            )
            # 인증 성공
            verification.is_verified = True
            verification.save()
            
            # 세션에 인증된 이메일 저장
            request.session['verified_email'] = email
            return JsonResponse({
                'success': True,
                'message': '이메일 인증이 완료되었습니다.'
            })
            
        except EmailVerification.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': '잘못된 인증 코드이거나 만료된 코드입니다.'
            })
    
    return JsonResponse({
        'success': False,
        'message': '잘못된 요청입니다.'
    })

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

@login_required # 로그인 후만 사용가능
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
