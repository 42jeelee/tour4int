from django.db import models

# Create your models here.
class BannerImage(models.Model):
    title = models.CharField(max_length=100, blank=True, help_text="배너 제목")
    path = models.CharField(max_length=255, help_text="배너 이미지 파일을 업로드하세요.")
    is_active = models.BooleanField(default=False, help_text="활성 상태 여부")

    def __str__(self):
        return self.title if self.title else f"배너 이미지 ({self.id})"