from django.db import models

# Create your models here.
class AreaCode(models.Model):
  area_code = models.IntegerField(primary_key=True)
  name = models.CharField(max_length=10, blank=False)
  image_url = models.CharField(max_length=255, default='/static/404_error.png')

  def __str__(self):
    return f"[{self.area_code}]{self.name}"


class SigunguCode(models.Model):
  id = models.AutoField(primary_key=True)
  sigungu_code = models.IntegerField(null=False)
  area_code = models.ForeignKey(AreaCode, on_delete=models.CASCADE)
  name = models.CharField(max_length=10, blank=False)

  def __str__(self):
    return f"[{self.sigungu_code}]{self.name}"
