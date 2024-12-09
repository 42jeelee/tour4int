from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
import random
import string

class User(AbstractUser):
    """
    사용자 모델
    username 필드: 이메일 주소로 사용
    email 필드: username과 동일한 이메일 주소
    password 필드: Django 기본 password 필드 사용
    """
    name = models.CharField('이름', max_length=10)
    nickname = models.CharField('닉네임', max_length=10)
    address = models.CharField('주소', max_length=100)
    created_at = models.DateTimeField('생성일', auto_now_add=True)
    updated_at = models.DateTimeField('수정일', auto_now=True)
    is_email_verified = models.BooleanField('이메일 인증 여부', default=False)

    class Meta:
        db_table = 'user'
        verbose_name = '사용자'
        verbose_name_plural = '사용자'

    def __str__(self):
        return f"{self.name} ({self.email})"

class EmailVerification(models.Model):
    """
    이메일 인증 코드 모델
    """
    email = models.EmailField('이메일')
    verification_code = models.CharField('인증 코드', max_length=6)
    created_at = models.DateTimeField('생성일', auto_now_add=True)
    expires_at = models.DateTimeField('만료일')
    is_verified = models.BooleanField('인증 여부', default=False)
    
    class Meta:
        db_table = 'email_verification'
        verbose_name = '이메일 인증'
        verbose_name_plural = '이메일 인증'

    def __str__(self):
        return f"{self.email} ({self.verification_code})"

    @classmethod
    def generate_verification_code(cls):
        """6자리 랜덤 인증 코드 생성"""
        return ''.join(random.choices(string.digits, k=6))

    @classmethod
    def create_verification(cls, email):
        """새로운 인증 코드 생성"""
        # 기존 인증 코드가 있다면 삭제
        cls.objects.filter(email=email).delete()
        
        # 새로운 인증 코드 생성
        verification_code = cls.generate_verification_code()
        expires_at = timezone.now() + timezone.timedelta(minutes=30)  # 30분 후 만료
        
        return cls.objects.create(
            email=email,
            verification_code=verification_code,
            expires_at=expires_at
        )
