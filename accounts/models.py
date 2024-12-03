from django.db import models
from django.contrib.auth.models import User as AuthUser

class User(models.Model):
    """
    사용자 추가 정보 모델
    """
    user_id = models.OneToOneField(
        AuthUser,
        on_delete=models.CASCADE,
        related_name='user_info'
    )
    name = models.CharField(max_length=10)
    nickname = models.CharField(max_length=10)
    address = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'user'  # 테이블 이름을 'user'로 지정

    def __str__(self):
        return f"{self.name} ({self.user_id.email})"

# Signal receivers 제거 - forms.py에서 처리하도록 변경
