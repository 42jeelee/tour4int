from django.db import models

# Create your models here.
class Category(models.Model):
  category = models.CharField(max_length=10, primary_key=True)
  content_type = models.IntegerField(null=False)
  name = models.CharField(max_length=20, blank=False)

  def __str__(self):
    return f"[{self.category}]{self.name}"
