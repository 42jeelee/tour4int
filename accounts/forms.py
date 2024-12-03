from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm, AuthenticationForm
from django.contrib.auth.models import User as AuthUser
from django.core.exceptions import ValidationError
from .models import User

class SignUpForm(UserCreationForm):
    """
    회원가입 폼 - 사용자 입력 데이터 검증
    """
    email = forms.EmailField(
        label='이메일', 
        max_length=255, 
        help_text='로그인에 사용할 이메일 주소를 입력해주세요.'
    )
    password1 = forms.CharField(
        label='비밀번호',
        widget=forms.PasswordInput,
        help_text='최소 8자 이상이어야 하며, 숫자와 특수문자를 포함해야 합니다.'
    )
    password2 = forms.CharField(
        label='비밀번호 확인',
        widget=forms.PasswordInput,
        help_text='비밀번호를 다시 입력해주세요.'
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

    class Meta:
        model = AuthUser
        fields = ('email', 'password1', 'password2', 'name', 'nickname', 'address')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if AuthUser.objects.filter(username=email).exists():
            raise ValidationError('이미 사용 중인 이메일 주소입니다.')
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['email']  # 이메일을 username으로 사용
        user.email = self.cleaned_data['email']
        
        if commit:
            user.save()
            # 추가 정보 저장
            User.objects.create(
                user_id=user,
                name=self.cleaned_data['name'],
                nickname=self.cleaned_data['nickname'],
                address=self.cleaned_data['address']
            )
        return user

class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label='아이디',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        label='비밀번호',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

class UserUpdateForm(forms.ModelForm):
    """
    사용자 정보 수정 폼
    """
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
        fields = ['name', 'nickname', 'address']

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