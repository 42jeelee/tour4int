from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.core.exceptions import ValidationError
from .models import User
from django.contrib.auth import authenticate

class SignUpForm(UserCreationForm):
    """
    회원가입을 처리하는 폼
    - 이메일, 비밀번호, 이름, 닉네임, 주소 정보를 입력받음
    - 이메일과 닉네임 중복 검사를 수행
    - 비밀번호 확인 기능 포함
    """
    email = forms.EmailField(
        label='이메일', 
        max_length=255
    )
    name = forms.CharField(
        label='이름',
        max_length=10
    )
    nickname = forms.CharField(
        label='닉네임', 
        max_length=10
    )
    address = forms.CharField(
        label='주소', 
        max_length=100
    )

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2', 'name', 'nickname', 'address')

    def __init__(self, *args, **kwargs):
        """
        폼 초기화 시 실행되는 메서드
        - 비밀번호 필드의 도움말 텍스트를 제거하여 깔끔한 UI 제공
        - 비밀번호 필드의 레이블을 한글로 변경
        """
        super().__init__(*args, **kwargs)
        # 비밀번호 필드의 help_text 제거
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None
        # 비밀번호 필드 레이블 변경
        self.fields['password1'].label = '비밀번호'
        self.fields['password2'].label = '비밀번호 확인'

    def clean_email(self):
        """
        이메일 중복 검사를 수행하는 메서드
        - 입력된 이메일이 이미 사용 중인지 확인
        - 중복된 경우 에러 메시지 표시
        """
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError('이미 사용 중인 이메일 주소입니다.')
        return email

    def clean_nickname(self):
        """
        닉네임 중복 검사를 수행하는 메서드
        - 입력된 닉네임이 이미 사용 중인지 확인
        - 중복된 경우 에러 메시지 표시
        """
        nickname = self.cleaned_data.get('nickname')
        if User.objects.filter(nickname=nickname).exists():
            raise ValidationError('이미 사용 중인 닉네임입니다.')
        return nickname

    def save(self, commit=True):
        """
        사용자 정보를 저장하는 메서드
        - 이메일을 아이디(username)로 사용
        - commit=True인 경우 즉시 데이터베이스에 저장
        """
        user = super().save(commit=False)
        user.username = self.cleaned_data['email']  # username을 email로 설정
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class CustomPasswordChangeForm(PasswordChangeForm):
    """
    비밀번호 변경을 처리하는 폼
    - 현재 비밀번호 확인
    - 새로운 비밀번호 입력 및 확인
    - 비밀번호 규칙 안내 텍스트 제공
    """
    def __init__(self, *args, **kwargs):
        """
        폼 초기화 시 실행되는 메서드
        - 비밀번호 필드의 도움말 텍스트를 간단하게 수정
        """
        super().__init__(*args, **kwargs)
        # 도움말 텍스트 간소화
        self.fields['old_password'].help_text = ''
        self.fields['new_password1'].help_text = '8자 이상의 영문자, 숫자, 특수문자 조합'
        self.fields['new_password2'].help_text = ''

class LoginForm(forms.Form):
    """
    로그인을 처리하는 폼
    - 이메일과 비밀번호를 입력받아 인증 처리
    - Bootstrap 스타일 적용을 위한 form-control 클래스 사용
    """
    email = forms.EmailField(
        label='이메일',
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        label='비밀번호',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        
        if email:
            # 먼저 이메일 존재 여부 확인
            if not User.objects.filter(email=email).exists():
                raise ValidationError('등록되지 않은 이메일입니다.')
            
            # 이메일이 존재하면 비밀번호 확인
            user = authenticate(username=email, password=password)
            if not user and password:
                raise ValidationError('비밀번호가 올바르지 않습니다.')
            
        return self.cleaned_data

class UserUpdateForm(forms.ModelForm):
    """
    사용자 정보 수정을 처리하는 폼
    - 이름, 닉네임, 주소 정보 수정 가능
    - 닉네임 중복 검사 수행
    - Bootstrap 스타일 적용
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nickname'].help_text = '다른 사용자와 중복되지 않는 별명을 입력해주세요 (최대 10자)'

    def clean_nickname(self):
        nickname = self.cleaned_data.get('nickname')
        if User.objects.exclude(pk=self.instance.pk).filter(nickname=nickname).exists():
            raise ValidationError('이미 사용 중인 닉네임입니다.')
        return nickname

    class Meta:
        model = User
        fields = ['name', 'nickname', 'address']
        labels = {
            'name': '이름',
            'nickname': '닉네임',
            'address': '주소',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'nickname': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
        }