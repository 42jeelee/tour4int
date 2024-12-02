from django import forms
from django.contrib.auth.forms import PasswordChangeForm, AuthenticationForm
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from .models import User

class SignUpForm(UserCreationForm):
    """
    회원가입 폼 - 사용자 입력 데이터 검증
    """
    # 추가 필드 정의
    email = forms.EmailField(
        label='이메일 주소', 
        max_length=255, 
        help_text='유효한 이메일 주소를 입력해주세요.'
    )
    name = forms.CharField(
        label='이름', 
        max_length=10, 
        help_text='실명을 입력해주세요.'
    )
    nickname = forms.CharField(
        label='닉네임', 
        max_length=10, 
        help_text='다른 사용자와 중복되지 않는 닉네임을 입력해주세요.'
    )
    address = forms.CharField(
        label='주소', 
        max_length=100, 
        help_text='대한민국 주소를 입력해주세요.'
    )
    password1 = forms.CharField(
        label='비밀번호', 
        widget=forms.PasswordInput,
        help_text='8자 이상의 안전한 비밀번호를 입력해주세요.'
    )
    password2 = forms.CharField(
        label='비밀번호 확인', 
        widget=forms.PasswordInput,
        help_text='앞서 입력한 비밀번호를 다시 입력해주세요.'
    )

    class Meta:
        model = User
        fields = ('email', 'name', 'nickname', 'address', 'password1', 'password2')

    def clean_nickname(self):
        """
        닉네임 중복 검사
        """
        nickname = self.cleaned_data.get('nickname')
        if User.objects.filter(nickname=nickname).exists():
            raise ValidationError('이미 사용 중인 닉네임입니다.')
        return nickname

    def clean_email(self):
        """
        이메일 중복 검사
        """
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError('이미 사용 중인 이메일 주소입니다.')
        return email

class LoginForm(AuthenticationForm):
    username = forms.EmailField(
        label='이메일',
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        label='비밀번호',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

class UserUpdateForm(forms.ModelForm):
    """
    사용자 정보 수정 폼
    """
    email = forms.EmailField(
        label='이메일',
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    name = forms.CharField(
        label='이름',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    nickname = forms.CharField(
        label='닉네임',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    address = forms.CharField(
        label='주소',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = ['email', 'name', 'nickname', 'address']

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.exclude(pk=self.instance.pk).filter(email=email).exists():
            raise ValidationError('이미 사용 중인 이메일입니다.')
        return email

    def clean_nickname(self):
        nickname = self.cleaned_data['nickname']
        if User.objects.exclude(pk=self.instance.pk).filter(nickname=nickname).exists():
            raise ValidationError('이미 사용 중인 닉네임입니다.')
        return nickname

User = get_user_model()

class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        label='기존 비밀번호',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )
    new_password1 = forms.CharField(
        label='새 비밀번호',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        help_text='최소 8자 이상, 숫자와 특수문자를 포함해야 합니다.'
    )
    new_password2 = forms.CharField(
        label='새 비밀번호 확인',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )

    class Meta:
        model = User
        fields = ['old_password', 'new_password1', 'new_password2']