from django.contrib import admin
from .models import BannerImage

@admin.register(BannerImage)
class BannerImageAdmin(admin.ModelAdmin):
    list_display = ('title', 'path', 'is_active')