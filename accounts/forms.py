from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.core.exceptions import ValidationError
from .models import User

class SignUpForm(UserCreationForm):
    """
    회원가입 폼
    """
    email = forms.EmailField(
        label='이메일', 
        max_length=255, 
        help_text='로그인에 사용할 이메일 주소를 입력해주세요.'
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

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError('이미 사용 중인 이메일 주소입니다.')
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['email']  # username을 email로 설정
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class CustomPasswordChangeForm(PasswordChangeForm):
    """
    비밀번호 변경 폼 커스터마이징
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 도움말 텍스트 간소화
        self.fields['old_password'].help_text = ''
        self.fields['new_password1'].help_text = '8자 이상의 영문자, 숫자, 특수문자 조합'
        self.fields['new_password2'].help_text = ''

class LoginForm(forms.Form):
    email = forms.CharField(
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
    class Meta:
        model = User
        fields = ['name', 'nickname', 'address']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'nickname': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
        }