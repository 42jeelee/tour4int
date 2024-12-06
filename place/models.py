from django.db import models
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

  start_time = models.DateTimeField(null=True)
  end_time = models.DateTimeField(null=True)

  is_detail = models.BooleanField(default=False)
  homepage_url = models.CharField(max_length=500, null=True)
  overview = models.TextField(null=True)

  updated_at = models.DateField(auto_now=True)
  created_at = models.DateField(auto_now_add=True)

  def __str__(self):
    return f"{self.title} ({self.address})"