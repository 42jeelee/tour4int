from django.db import models

# Create your models here.
class Category(models.Model):
  category = models.CharField(max_length=10, null=False)
  content_type = models.IntegerField(null=False)
  name = models.CharField(max_length=20, null=False)