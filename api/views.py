from django.http import JsonResponse
from django.db import transaction
from django.forms.models import model_to_dict
from areacode.models import AreaCode, SigunguCode
from category.models import Category
from place.models import Place
from api.apilog import logType, logging_fetch_log, has_fetch, get_all_log
from . import api
from datetime import datetime
from api.exceptions import ApiResultException

CONTANT_TYPE = [12, 14, 15, 25]

# Create your views here.
def init_all(request):
  context = {"result": "success"}

  init_category(request)
  init_areacode(request)
  init_sigungucode(request)
  init_place(request)
  return JsonResponse(context)

def init_areacode(request):
  context = {}
  try:
    with transaction.atomic():
      data = api.get_all_areacode()

      AreaCode.objects.all().delete()

      context['modifed_count'] = 0
      for d in data:
        area_code = d['code']
        name = d['name']
        image_url = f"/static/images/area-image/{area_code}.jpg"

        AreaCode.objects.create(area_code=area_code, name=name, image_url=image_url)
        context['modifed_count'] += 1

      context['result'] = "success"
      context['data'] = data

      context['log_info'] = logging_fetch_log(logType.AREACODE, context)
  except Exception as e:
    context['result'] = 'fail'
    context['error'] = str(e)

  return JsonResponse(context)

def init_sigungucode(request):
  context = {'data': []}
  area_codes = AreaCode.objects.all()

  try:
    with transaction.atomic():

      SigunguCode.objects.all().delete()

      context['modifed_count'] = 0
      for c in area_codes:
        curr_list = api.get_all_sigungucode(c.area_code)
        context['data'] += curr_list

        area_code = AreaCode.objects.get(area_code=c.area_code)

        for s in curr_list:
          sigungu_code = s['code']
          name = s['name']

          SigunguCode.objects.create(sigungu_code=sigungu_code, area_code=area_code, name=name)
          context['modifed_count'] += 1

      context['result'] = 'success'

      context['log_info'] = logging_fetch_log(logType.SIGUNGUCODE, context)
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

      context['modifed_count'] = 0
      for d in data:
        category = d['code']
        content_type = d['content_type']
        name = d['name']

        Category.objects.create(category=category, content_type=content_type, name=name)
        context['modifed_count'] += 1

    context['result'] = "success"
    context['data'] = data

    context['log_info'] = logging_fetch_log(logType.CATEGORY, context)
  except Exception as e:
    context['result'] = 'fail'
    context['error'] = str(e)
  return JsonResponse(context)

def init_place(request):

  if not has_fetch(logType.CATEGORY) and not has_fetch(logType.SIGUNGUCODE):
    context = {
      'result': 'fail',
      'error': "We don't have category or sigungucode"
    }
    return JsonResponse(context)

  content_types = [12, 14, 25]
  data = api.get_all_place(content_types=content_types)

  try:
    with transaction.atomic():
      Place.objects.filter(category__content_type__in = content_types).delete()
      context = insert_place(data)

      if context['result'] == 'fail': raise ApiResultException("Fail from insert place", context)
    
  except ApiResultException as e:
    return JsonResponse(e.context)

  return JsonResponse(context)

def get_event(request):

  if not has_fetch(logType.CATEGORY) and not has_fetch(logType.SIGUNGUCODE):
    context = {
      'result': 'fail',
      'error': "We don't have category or sigungucode"
    }
    return JsonResponse(context)

  eventime = datetime.now().replace(day=1).date().strftime(f'%Y%m%d')
  event_data = api.get_event_info(eventime)

  try:
    with transaction.atomic():
      Place.objects.filter(category__content_type=15).delete()
      context = insert_place(event_data, isEvent=True)

      if context.get('result') == 'fail': raise ApiResultException("Fail from insert place", context)

  except ApiResultException as e:
    return JsonResponse(e.context)

  return JsonResponse(context)

def get_place(request):
  content_types = [12, 14, 25]
  if not has_fetch(logType.PLACE):
    return init_place(request)
  else:
    data = api.modify_all_place(content_types=content_types)
    context = insert_place(data)

  return JsonResponse(context)

def get_info(contentid):
  try:
    place = Place.objects.get(place_id=contentid)

    info_data = api.get_place_common_info(place.place_id)
    info_data.update(api.get_place_detail_info(place.place_id, place.category.content_type))

    place_info = {
    'accomcount': info_data.get('accomcount', ''),
    'chkbabycarriage': info_data.get('chkbabycarriage', ''),
    'chkcreditcard': info_data.get('chkcreditcard', ''),
    'chkpet': info_data.get('chkpet', ''),
    'expagerange': info_data.get('expagerange', ''),
    'expguide': info_data.get('expguide', ''),
    'heritage1': info_data.get('heritage1', ''),
    'heritage2': info_data.get('heritage2', ''),
    'heritage3': info_data.get('heritage3', ''),
    'infocenter': info_data.get('infocenter', ''),
    'opendate': info_data.get('opendate', ''),
    'parking': info_data.get('parking', ''),
    'restdate': info_data.get('restdate', ''),
    'useseason': info_data.get('useseason', ''),
    'usetime': info_data.get('usetime', ''),
    'accomcountculture': info_data.get('accomcountculture', ''),
    'chkbabycarriageculture': info_data.get('chkbabycarriageculture', ''),
    'chkcreditcardculture': info_data.get('chkcreditcardculture', ''),
    'chkpetculture': info_data.get('chkpetculture', ''),
    'discountinfo': info_data.get('discountinfo', ''),
    'infocenterculture': info_data.get('infocenterculture', ''),
    'parkingculture': info_data.get('parkingculture', ''),
    'parkingfee': info_data.get('parkingfee', ''),
    'restdateculture': info_data.get('restdateculture', ''),
    'usefee': info_data.get('usefee', ''),
    'usetimeculture': info_data.get('usetimeculture', ''),
    'scale': info_data.get('scale', ''),
    'spendtime': info_data.get('spendtime', ''),
    'agelimit': info_data.get('agelimit', ''),
    'bookingplace': info_data.get('bookingplace', ''),
    'discountinfofestival': info_data.get('discountinfofestival', ''),
    'eventenddate': info_data.get('eventenddate', ''),
    'eventhomepage': info_data.get('eventhomepage', ''),
    'eventplace': info_data.get('eventplace', ''),
    'eventstartdate': info_data.get('eventstartdate', ''),
    'festivalgrade': info_data.get('festivalgrade', ''),
    'placeinfo': info_data.get('placeinfo', ''),
    'playtime': info_data.get('playtime', ''),
    'program': info_data.get('program', ''),
    'spendtimefestival': info_data.get('spendtimefestival', ''),
    'sponsor1': info_data.get('sponsor1', ''),
    'sponsor1tel': info_data.get('sponsor1tel', ''),
    'sponsor2': info_data.get('sponsor2', ''),
    'sponsor2tel': info_data.get('sponsor2tel', ''),
    'subevent': info_data.get('subevent', ''),
    'usetimefestival': info_data.get('usetimefestival', ''),
    'distance': info_data.get('distance', ''),
    'infocentertourcourse': info_data.get('infocentertourcourse', ''),
    'schedule': info_data.get('schedule', ''),
    'taketime': info_data.get('taketime', ''),
    'theme': info_data.get('theme', ''),
    }

    for f, v in place_info.items():
      setattr(place, f, v)

    place.is_detail = True
    place.save()
    return model_to_dict(place)
  except Exception as e:
    raise e

def get_place_info(request, contentid):
  try:
    place = get_info(contentid)
    context = {
      'result': 'success',
      'data': model_to_dict(place),
    }
    return JsonResponse(context)
  except Exception as e:
    return JsonResponse({"result": "fail", "error": e})


def insert_place(data, isEvent=False):
  context = {}
  try:
    with transaction.atomic():

      category_all = Category.objects.all()
      areacode_all = AreaCode.objects.all()
      sigungucode_all = SigunguCode.objects.all()

      if category_all and sigungucode_all:
        context['modifed_count'] = 0
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

          if Place.objects.filter(place_id=place_id).exists():
            Place.objects.filter(place_id=place_id).update(**place_data)
          else:
            Place.objects.create(place_id=place_id, **place_data)

          context['modifed_count'] += 1

        context['result'] = "success"
        context['data'] = data

        if isEvent: context['log_info'] = logging_fetch_log(logType.EVENT, context)
        else: context['log_info'] = logging_fetch_log(logType.PLACE, context)
      else:
        context['result'] = "fail"
        context['error'] = "We don't have category or sigungucode"
  except Exception as e:
    context['result'] = 'fail'
    context['error'] = str(e)

  return context

def get_logged(request):
  return JsonResponse(get_all_log())
