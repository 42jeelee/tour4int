from django.db import models

# Create your models here.
class AreaCode(models.Model):
  area_code = models.CharField(max_length=5, primary_key=True)
  name = models.CharField(max_length=10, blank=False)
  region_code = models.CharField(max_length=2, blank=False)
  region_name = models.CharField(max_length=2, blank=False)

  def __str__(self):
    return f"[{self.area_code}]{self.name}"
