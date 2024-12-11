from django.shortcuts import render
from place.models import Place
from accounts.models import User
from areacode.models import AreaCode, SigunguCode
from category.models import Category
# Ajax
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from django.core import serializers # json타입 db에서 get으로 받을때


# Create your views here.
def touradmin(request):
  context = {
    'users': User.objects.all(),
    'AreaCodes': AreaCode.objects.filter(),
    'events': Place.objects.filter(category__content_type = 15),
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