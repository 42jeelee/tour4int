from django.contrib import admin
from api.models import ApiFetchLog

# Register your models here.
@admin.register(ApiFetchLog)
class ApiFetchLogAdmin(admin.ModelAdmin):
  list_display = ['is_category', 'is_areacode', 'is_sigungucode', 'is_place', 'is_event']

  def get_readonly_fields(self, request, obj=None):
    return [ f.name for f in ApiFetchLog._meta.fields ]
  
  def has_delete_permission(self, request, obj=None):
    return False

  def has_change_permission(self, request, obj=None):
    return False
