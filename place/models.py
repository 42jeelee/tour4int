from django.db import models
from accounts.models import User
from areacode.models import SigunguCode
from category.models import Category

# Create your models here.
class Place(models.Model):
  place_id = models.IntegerField(primary_key=True)

  category = models.ForeignKey(Category, on_delete=models.CASCADE)
  sigungu_code = models.ForeignKey(SigunguCode, on_delete=models.CASCADE)

  title = models.CharField(max_length=100, null=False)
  address = models.CharField(max_length=100, null=False)
  map_x = models.CharField(max_length=20, null=False)
  map_y = models.CharField(max_length=20, null=False)
  
  tel = models.CharField(max_length=13)
  image = models.CharField(max_length=100)
  thumb_img = models.CharField(max_length=100)

  start_time = models.DateField(null=True)
  end_time = models.DateField(null=True)

  is_detail = models.BooleanField(default=False)
  homepage_url = models.CharField(max_length=500, null=True)
  overview = models.TextField(null=True)

  updated_at = models.DateTimeField(auto_now=True)
  created_at = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return f"{self.title} ({self.address})"
  
  @property
  def like_count(self):
      """좋아요 수 반환"""
      return self.likes.count()
  
class Like(models.Model):
    post = models.ForeignKey(Place, on_delete=models.CASCADE, related_name='likes')  # 어떤 게시물에 대한 좋아요인지
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # 어떤 사용자가 좋아요를 눌렀는지
    created_at = models.DateTimeField(auto_now_add=True)  # 좋아요를 누른 시간

    class Meta:
        unique_together = ('post', 'user')  # 한 사용자가 같은 게시물에 좋아요를 중복으로 누르지 못하도록 설정

    def __str__(self):
        return f"{self.user.username} likes {self.post.title}"