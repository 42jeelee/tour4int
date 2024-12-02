from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class User(AbstractUser):
    # 기본 AbstractUser에서 username 대신 email 사용
    username = None
    email = models.EmailField(unique=True)
    
    # 추가 필드들
    nickname = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=10)
    address = models.CharField(max_length=100)
    
    # 로그인에 사용할 필드 지정
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nickname', 'name']

    # related_name 추가
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name='accounts_user_set',
        related_query_name='accounts_user',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='accounts_user_set',
        related_query_name='accounts_user',
    )

    def __str__(self):
        return self.email
