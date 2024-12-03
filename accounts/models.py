from django.db import models
from django.contrib.auth.models import AbstractUser

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

    class Meta:
        db_table = 'user'
        verbose_name = '사용자'
        verbose_name_plural = '사용자'

    def __str__(self):
        return f"{self.name} ({self.email})"
