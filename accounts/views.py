from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.http import JsonResponse
from .forms import SignUpForm, LoginForm, UserUpdateForm, CustomPasswordChangeForm
from .models import User
from django.conf import settings
from place.models import Place, Like

def signup_view(request):
    """
    회원가입 뷰 - 새로운 사용자 등록
    """
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, '환영합니다! 회원가입이 완료되었습니다. 즐거운 여행 되세요!')
            return redirect('index')
    else:
        form = SignUpForm()
    
    return render(request, 'accounts/signup.html', {'form': form})

def send_verification_code(request):
    """
    이메일 중복 체크
    """
    if request.method == 'POST':
        email = request.POST.get('email')
        if email:
            # 이메일 중복 검사
            if User.objects.filter(email=email).exists():
                return JsonResponse({
                    'success': False,
                    'message': '이미 사용 중인 이메일 주소입니다.'
                })
            return JsonResponse({
                'success': True,
                'message': '사용 가능한 이메일입니다.'
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
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(request, email=email, password=password)
            if user is not None:
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

@login_required
def update_profile(request):
    """
    프로필 업데이트 뷰
    """
    if request.method == 'POST':
        user = request.user
        user.name = request.POST.get('name')
        user.nickname = request.POST.get('nickname')
        user.address = request.POST.get('address')
        user.save()
        messages.success(request, '회원정보가 성공적으로 수정되었습니다.')
        return redirect('accounts:mypage')
    return redirect('accounts:mypage')

@login_required
def change_password(request):
    """
    비밀번호 변경 뷰
    """
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # 세션 유지
            messages.success(request, '비밀번호가 성공적으로 변경되었습니다.')
        else:
            if 'old_password' in form.errors:
                messages.error(request, '현재 비밀번호가 올바르지 않습니다.')
            else:
                error_message = """
                비밀번호는 다음 조건을 만족해야 합니다:
                • 8자 이상
                • 영문자 포함
                • 숫자 포함
                • 특수문자 포함
                • 비밀번호 확인과 일치
                """
                messages.error(request, error_message)
    return redirect('accounts:mypage')

@login_required
def delete_account(request):
    if request.method == 'POST':
        user = request.user
        logout(request)  # Django의 내장 로그아웃
        user.delete()  # Django의 내장 delete() 메서드
        messages.success(request, '회원탈퇴가 완료되었습니다.')
        return redirect('/')  # 메인 페이지로 리다이렉트
    return redirect('accounts:mypage')

@login_required
def get_history(request):
    context = {}
    user = request.user

    if user.place_history is not None and len(user.place_history) > 0:
        places = user.place_history.split(',')
        db_data = Place.objects.filter(place_id__in=places).values('place_id', 'title', 'sigungu_code__area_code__name', 'sigungu_code__name', 'image')

        data = [ {'id': item['place_id'], 'area': f"{item['sigungu_code__area_code__name']} {item['sigungu_code__name']}", 'title': item['title'], 'image': item['image']} for item in db_data ]

        sorted_data = sorted(data, key=lambda d: places.index(str(d['id'])))

        if len(sorted_data) > 0:
            context['result'] = 'success'
            context['data'] = list(sorted_data)
        else:
            context['result'] = 'fail'
            context['error'] = 'Not Found.'
    else:
        context['result'] = 'success'
        context['data'] = []

    return JsonResponse(context)

@login_required
def get_like(request):
    context = {}
    user = request.user
    likes = Like.objects.filter(user=user)
    
    data = [ {'id': l.place.place_id, 'area': f"{l.place.sigungu_code.area_code.name} {l.place.sigungu_code.name}", 'title': l.place.title, 'image': l.place.image} for l in likes ]

    context['result'] = "success"
    context['data'] = data

    return JsonResponse(context)