from django.db import models

# Create your models here.
class ApiFetchLog(models.Model):
  id = models.AutoField(primary_key=True)

  is_category = models.BooleanField(default=False, null=False)
  category_num = models.IntegerField(default=0, null=False)
  modify_category = models.DateTimeField(null=True)

  is_areacode = models.BooleanField(default=False, null=False)
  areacode_num = models.IntegerField(default=0, null=False)
  modify_areacode = models.DateTimeField(null=True)

  is_sigungucode = models.BooleanField(default=False, null=False)
  sigungu_num = models.IntegerField(default=0, null=False)
  modify_sigungucode = models.DateTimeField(null=True)

  is_place = models.BooleanField(default=False, null=False)
  place_num = models.IntegerField(default=0, null=False)
  modify_place = models.DateTimeField(null=True)

  is_event = models.BooleanField(default=False, null=False)
  event_num = models.IntegerField(default=0, null=False)
  modify_event = models.DateTimeField(null=True)

  def __str__(self):
    return f"place({self.place_num + self.event_num})"