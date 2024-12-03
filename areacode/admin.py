from django.contrib import admin
from areacode.models import AreaCode

# Register your models here.
@admin.register(AreaCode)
class AreaCodeAdmin(admin.ModelAdmin):
  list_display = ['area_code', 'name']
