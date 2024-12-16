from django.contrib import admin
from place.models import Place, Like

# Register your models here.
@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
  list_display = ['place_id', 'title']

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
  list_display = ['place', 'user']