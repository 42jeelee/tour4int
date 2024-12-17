from django.contrib import admin
from place.models import Place, Like, Views

# Register your models here.
@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
  list_display = ['place_id', 'title']

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
  list_display = ['place', 'user']

@admin.register(Views)
class PlaceAdmin(admin.ModelAdmin):
  list_display = ['place_id', 'count']
