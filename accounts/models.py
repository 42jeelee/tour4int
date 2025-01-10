from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    """
    사용자 모델
    username 필드: 이메일 주소로 사용
    email 필드: username과 동일한 이메일 주소
    password 필드: Django 기본 password 필드 사용
    """
    email = models.EmailField('이메일', unique=True, blank=False)
    name = models.CharField('이름', max_length=10, blank=False)
    nickname = models.CharField('닉네임', max_length=10, blank=False)
    address = models.CharField('주소', max_length=100, null=True, blank=True)

    is_staff = models.BooleanField('스탭여부', default=False)
    is_superuser = models.BooleanField('관리자여부', default=False)
    is_active = models.BooleanField('활성여부', default=True)

    updated_at = models.DateTimeField('수정일', auto_now=True)
    created_at = models.DateTimeField('생성일', auto_now_add=True)

    place_history = models.CharField(
        '방문기록',
        max_length=120,
        help_text= '","로 구분하는 place_id (최대 10개)',
        null=True,
        blank=True,
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'nickname']
    objects = UserManager()

    def add_place_history(self, place_id):
        if self.place_history:
            place_ids = self.place_history.split(',')

            if place_id not in place_ids:
                place_ids.insert(0, place_id)

                if len(place_ids) > 10: place_ids.pop()

                self.place_history = ','.join(place_ids)
            else:
                place_ids.remove(place_id)
                place_ids.insert(0, place_id)
                self.place_history = ','.join(place_ids)
        else:
            self.place_history = place_id

        self.save()

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.email})"
    
    class Meta:
        db_table = 'user'
        verbose_name = '사용자'
        verbose_name_plural = '사용자'
