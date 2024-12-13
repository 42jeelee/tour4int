from django.shortcuts import render
from place.models import Place
from accounts.models import User
from areacode.models import AreaCode, SigunguCode
from touradmin.models import BannerImage
from category.models import Category
from api import api
import os
from django.conf import settings
# Ajax
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from django.core import serializers # json타입 db에서 get으로 받을때


# Create your views here.
def touradmin(request):
  image_dir = os.path.join(settings.STATIC_ROOT or os.path.join(settings.BASE_DIR, 'static'), 'images/main-banners')
  image_files = []

  if os.path.exists(image_dir):
    image_files = [
        {"name": file_name, "path": f'images/main-banners/{file_name}'}
        for file_name in os.listdir(image_dir)
        if file_name.lower().endswith(('.jpg', '.jpeg', '.png', '.gif'))
    ]

  context = {
    'users': User.objects.all(),
    'AreaCodes': AreaCode.objects.filter(),
    'events': Place.objects.filter(category__content_type = 15),
    'banners': image_files,
    'banners_active' : BannerImage.objects.all()
  }
  return render(request, 'touradmin.html', context)

# 각 지역별 관광지 데이터
def get_place(request):
  context = {}
  search = request.POST.get('areaCode')
  if search:
    area_data = Place.objects.filter(category__content_type = 12, sigungu_code__area_code__area_code = search)
    context['areaCode'] = list(area_data.values())
    context['result'] = 'success'
  else:
    context['result'] = 'fail'
  return JsonResponse(context)

# 각 지역별 이벤트 데이터
def get_event(request):
  context = {}
  search = request.POST.get('areaCode')
  if search:
    event_data = Place.objects.filter(category__content_type = 15, sigungu_code__area_code__area_code = search)
    context['event'] = list(event_data.values())
    context['result'] = 'success'
  else:
    context['result'] = 'fail'
  return JsonResponse(context)

# place 수정 타겟 데이터
def get_view(request):
  content = {}
  if request.method == 'POST':
    content_id = request.POST.get('no')
    content_data = Place.objects.get(place_id=content_id)
    if content_data.is_detail:
      content['result'] = "success"
      content['view'] = serializers.serialize('json', [content_data])
    else:
      overview = api.get_place_info(content_id)
      content_data.overview = overview['overview']
      content_data.homepage_url = overview['homepage']
      content_data.is_detail = True
      content_data.save()
      content['result'] = 'info_success'
      content['view'] = serializers.serialize('json', [content_data])
  else:
    content['result'] = 'fail'
  return JsonResponse(content)

# place 수정하기
def update(request):
  content = {}
  if request.method == 'POST':
    content_id = request.POST.get('target')
    title = request.POST.get('title')
    address = request.POST.get('address')
    tel = request.POST.get('tel')
    image = request.POST.get('image')
    thumb_img = request.POST.get('thumb_img')
    homepage_url = request.POST.get('homepage_url')
    overview = request.POST.get('overview')
    data = Place.objects.get(place_id=content_id)
    data.title = title
    data.address = address
    data.tel = tel
    data.image = image
    data.thumb_img = thumb_img
    data.homepage_url = homepage_url
    data.overview = overview
    data.save()
    content['result'] = 'success'
    content['view'] = serializers.serialize('json', [data])
  else:
    content['result'] = 'fail'
  return JsonResponse(content)

def get_user_view(request):
  content = {}
  if request.method == "POST":
    email = request.POST.get('email')
    user = User.objects.filter(email=email)
    content['result'] = 'success'
    content['view'] = serializers.serialize('json', [user[0]])
  return JsonResponse(content)





