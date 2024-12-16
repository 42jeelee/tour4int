from django.shortcuts import render
from areacode.models import AreaCode
from place.models import Place
from django.utils import timezone
from touradmin.models import BannerImage
import os
from django.conf import settings

# Create your views here.
def index(request):
  today = timezone.now()
  area_codes = AreaCode.objects.all()
  events = Place.objects.filter(category__content_type=15, end_time__gt=today).order_by("end_time")[:10]

  # 실제 존재하는 배너 이미지만 리스트에 추가
  banners = BannerImage.objects.filter(is_active=True)
  banner_images = []
  for banner in banners:
    banner_images.append(banner.path)
#   for i in range(1, 4):
#       image_path = f'images/main-banners/main_{i}.jpg'
#       if os.path.exists(os.path.join(settings.STATIC_ROOT or os.path.join(settings.BASE_DIR, 'static'), image_path)):
#           banner_images.append(image_path)

  return render(request, 'index.html', context={
      "area_codes": area_codes, 
      "events": events, 
      "today": today,
      "banner_images": banner_images
  })
