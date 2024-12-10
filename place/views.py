from django.shortcuts import render
from django.http import JsonResponse
from django.core.paginator import Paginator
from areacode.models import SigunguCode
from category.models import Category
from place.models import Place
import logging

logger = logging.getLogger(__name__)
from api import api

# Create your views here.
def local(request, areacode):
  tour_list = Place.objects.all().filter(sigungu_code__area_code=areacode, category__content_type=12).order_by('-thumb_img', '-updated_at')
  event_list = Place.objects.all().filter(sigungu_code__area_code=areacode, category__content_type=15).order_by('-thumb_img', '-start_time')
  print(len(tour_list))
  suggestion_tour = tour_list[:4]
  print(len(suggestion_tour))
  suggestion_event = event_list[:5]
  context = {
    'areacode': areacode,
    'tour_list': suggestion_tour,
    'event_list': suggestion_event
  }
  return render(request, 'local.html', context)

def view(request, areacode, content_id):
  context = {}
  range_offset = 0.004
  content_data = Place.objects.filter(place_id=content_id)
  context = {'around':''}
  context = {'len':0}
  if len(content_data):
    around_data = Place.objects.filter(sigungu_code__area_code=areacode,
      map_x__gte=float(content_data[0].map_x) - range_offset,  # map_x가 기준값 - 0.004 이상
      map_x__lte=float(content_data[0].map_x) + range_offset,  # map_x가 기준값 + 0.004 이하
      map_y__gte=float(content_data[0].map_y) - range_offset,  # map_y가 기준값 - 0.004 이상
      map_y__lte=float(content_data[0].map_y) + range_offset   # map_y가 기준값 + 0.004 이하
    )
    if content_data[0].is_detail:
      context['result'] = "success"
      context['data'] = content_data[0]
    else:
      overview = api.get_place_info(content_id)
      content_data[0].overview = overview['overview']
      content_data[0].homepage_url = overview['homepage']
      content_data[0].is_detail = True
      content_data[0].save()
      context['result'] = 'info_success'
      context['data'] = content_data[0]
    if around_data:
      context['around'] = around_data
      context['len'] = len(around_data)
      print(around_data)
  return render(request, 'view.html', context)