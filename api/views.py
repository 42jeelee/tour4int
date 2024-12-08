from django.http import JsonResponse
from django.db import transaction
from areacode.models import AreaCode, SigunguCode
from category.models import Category
from place.models import Place
from . import api
from datetime import datetime

CONTANT_TYPE = [12, 14, 15, 25]

# Create your views here.
def init_all(request):
  context = {"result": "success"}

  init_category(request)
  init_areacode(request)
  init_sigungucode(request)
  init_place(request)
  return JsonResponse(context)

def init_place(request):
  content_types = [12, 14, 25]
  data = api.get_all_place(content_types=content_types)
  context = insert_place(data, content_types=content_types)

  return JsonResponse(context)

def init_areacode(request):
  context = {}
  try:
    with transaction.atomic():
      data = api.get_all_areacode()

      AreaCode.objects.all().delete()

      for d in data:
        area_code = d['code']
        name = d['name']
        image_url = f"/static/images/area-image/{area_code}.jpg"

        AreaCode.objects.create(area_code=area_code, name=name, image_url=image_url)

      context['result'] = "success"
      context['data'] = data
  except Exception as e:
    context['result'] = 'fail'
    context['error'] = str(e)

  return JsonResponse(context)

def init_sigungucode(request):
  context = {'data': []}
  area_codes = AreaCode.objects.all()

  try:
    with transaction.atomic():
      for c in area_codes:
        curr_list = api.get_all_sigungucode(c.area_code)
        context['data'] += curr_list

        area_code = AreaCode.objects.get(area_code=c.area_code)

        for s in curr_list:
          sigungu_code = s['code']
          name = s['name']

          SigunguCode.objects.create(sigungu_code=sigungu_code, area_code=area_code, name=name)

      context['result'] = 'success'
  except Exception as e:
    context['result'] = 'fail'
    context['error'] = str(e)
    del context['data']

  return JsonResponse(context)


def init_category(request):
  context  = {}
  try:
    with transaction.atomic():
      data = api.get_all_category(content_types=CONTANT_TYPE)

      Category.objects.all().delete()

      for d in data:
        category = d['code']
        content_type = d['content_type']
        name = d['name']

        Category.objects.create(category=category, content_type=content_type, name=name)

    context['result'] = "success"
    context['data'] = data
  except Exception as e:
    context['result'] = 'fail'
    context['error'] = str(e)
  return JsonResponse(context)

# 이벤트 정보
def get_event(request):
  context = {}
  eventime = datetime.now().replace(day=1).date().strftime(f'%Y%m%d')
  try:
    with transaction.atomic():

      category_all = Category.objects.all()
      areacode_all = AreaCode.objects.all()
      sigungucode_all = SigunguCode.objects.all()

      if category_all and sigungucode_all:
        data = api.get_all_place(content_types=[15])
        Place.objects.filter(category__content_type = 15).delete()

        event_data = api.get_event_info(eventime)

        for i in data:
          place_id = i.get('contentid', '')
          start_time = end_time = None
          for event in event_data:
            if place_id == event['contentid']:
              if event['eventstartdate'] != '': start_time = event['eventstartdate']
              if event['eventenddate'] != '': end_time = event['eventenddate']
              break
          if start_time is None: continue
          
          areacode = i.get('areacode', '')
          sigungucode = i.get('sigungucode', '')
          category_id = i.get('cat2', '')

          map_x = i.get('mapx', '')
          map_y = i.get('mapy', '')
          
          if any(i == '' for i in [areacode, sigungucode, category_id, map_x, map_y]):
            continue
          
          category = category_all.filter(category=category_id)
          if len(category) == 0:
            continue

          category = category[0]

          area_code = areacode_all.get(area_code=areacode)
          sigungu_code = sigungucode_all.get(sigungu_code=sigungucode, area_code=area_code)

          title = i.get('title', '')
          address = i.get('addr1', '') + i.get('addr2', '')
          map_x = i.get('mapx', '')
          map_y = i.get('mapy', '')

          tel = i.get('tel', '')
          image = i.get('firstimage', '')
          thumb_img = i.get('firstimage2', '')

          modified_time = i.get('modifiedtime', '')
          created_time = i.get('createdtime', '')

          if modified_time != '': modified_time = datetime.strptime(modified_time, '%Y%m%d%H%M%S')
          if created_time != '': created_time = datetime.strptime(created_time, '%Y%m%d%H%M%S')

          Place.objects.create(place_id=place_id, category=category, \
            sigungu_code=sigungu_code, title=title, address=address, \
            map_x=map_x, map_y=map_y, tel=tel, image=image, thumb_img=thumb_img,\
            updated_at=modified_time, created_at=created_time,\
            start_time=start_time, end_time=end_time)

        context['result'] = "success"
        context['data'] = data
      else:
        context['result'] = "fail"
        context['error'] = "We don't have category or sigungucode"
  except Exception as e:
    context['result'] = 'fail'
    context['error'] = str(e)
  return JsonResponse(context)

# overview
def get_pinfo(request):
  context = {}
  context['result'] = "success"
  context['data'] = api.get_place_info(126508, 12)
  return JsonResponse(context)

def insert_place(data, content_types=CONTANT_TYPE, isEvent=False):
  context = {}
  try:
    with transaction.atomic():

      category_all = Category.objects.all()
      areacode_all = AreaCode.objects.all()
      sigungucode_all = SigunguCode.objects.all()

      if category_all and sigungucode_all:
        Place.objects.filter(category__content_type__in = content_types).delete()
        for i in data:
          areacode = i.get('areacode', '')
          sigungucode = i.get('sigungucode', '')
          category_id = i.get('cat2', '')

          map_x = i.get('mapx', '')
          map_y = i.get('mapy', '')

          eventstartdate = i.get('eventstartdate', '')
          eventenddate = i.get('eventenddate', '')

          if isEvent and eventstartdate == '':
            continue
          
          if any(i == '' for i in [areacode, sigungucode, category_id, map_x, map_y]):
            continue

          place_id = i.get('contentid', '')
          
          category = category_all.filter(category=category_id)
          if len(category) == 0:
            continue

          category = category[0]

          area_code = areacode_all.get(area_code=areacode)
          sigungu_code = sigungucode_all.get(sigungu_code=sigungucode, area_code=area_code)

          title = i.get('title', '')
          address = i.get('addr1', '') + i.get('addr2', '')
          map_x = i.get('mapx', '')
          map_y = i.get('mapy', '')

          tel = i.get('tel', '')
          image = i.get('firstimage', '')
          thumb_img = i.get('firstimage2', '')

          modified_time = i.get('modifiedtime', '')
          created_time = i.get('createdtime', '')

          if modified_time != '': modified_time = datetime.strptime(modified_time, '%Y%m%d%H%M%S')
          if created_time != '': created_time = datetime.strptime(created_time, '%Y%m%d%H%M%S')

          place_data = {
            'place_id': place_id,
            'category': category,
            'sigungu_code': sigungu_code,
            'title': title,
            'address': address,
            'map_x': map_x,
            'map_y': map_y,
            'tel': tel,
            'image': image,
            'thumb_img': thumb_img,
            'updated_at': modified_time,
            'created_at': created_time
          }

          if isEvent:
            place_data.update({
              'start_time': eventstartdate,
              'end_time': eventenddate,
            })

          Place.objects.create(**place_data)

        context['result'] = "success"
        context['data'] = data
      else:
        context['result'] = "fail"
        context['error'] = "We don't have category or sigungucode"
  except Exception as e:
    context['result'] = 'fail'
    context['error'] = str(e)

  return context