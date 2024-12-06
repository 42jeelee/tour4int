from django.contrib import admin
from areacode.models import AreaCode
from areacode.models import SigunguCode

# Register your models here.
@admin.register(AreaCode)
class AreaCodeAdmin(admin.ModelAdmin):
  list_display = ['area_code', 'name']

@admin.register(SigunguCode)
class AreaCodeAdmin(admin.ModelAdmin):
  list_display = ['id', 'sigungu_code', 'name']
