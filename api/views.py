from django.http import JsonResponse
from django.db import transaction
from areacode.models import AreaCode
from category.models import Category
from place.models import Place
from . import api
from datetime import datetime

CONTANT_TYPE = [12, 14, 15, 25]

# Create your views here.
def get_place(request):
  context = {}
  try:
    with transaction.atomic():

      category_check = Category.objects.all()
      areacode_check = AreaCode.objects.all()
      if category_check and areacode_check:
        data = api.get_all_place(CONTANT_TYPE)

        Place.objects.all().delete()

        for i in data:
          for j in i:
            if j['areacode'] == '' or j['sigungucode'] == '': continue
            region_code = f"{int(j['areacode']):02d}"
            area_code = f"{region_code}_{int(j['sigungucode']):02d}"
            place_id = int(j['contentid'])
            category = Category.objects.filter(category=j['cat2'])
            area_code2 = AreaCode.objects.filter(area_code=area_code)
            title = j['title']
            address = j['addr1'] + j['addr2']
            map_x = j['mapx']
            map_y = j['mapy']
            tel = j['tel']
            image = j['firstimage']
            thumb_img = j['firstimage2']
            modified_time = datetime.strptime(j['modifiedtime'], '%Y%m%d%H%M%S')
            createdtime = datetime.strptime(j['createdtime'], '%Y%m%d%H%M%S')
            start_time = ''
            end_time = ''
            if 'eventstartdate' in j.keys():
              start_time = datetime.strptime(j['eventstartdate'], '%Y%m%d%H%M%S')
              if j['eventenddate'] != '':
                end_time = datetime.strptime(j['eventenddate'], '%Y%m%d%H%M%S')
            if area_code2 and category:
              if start_time == '' and end_time =='':
                Place.objects.create(place_id=place_id, category=category[0], area_code=area_code2[0], title=title, address=address, map_x=map_x, map_y=map_y, tel=tel, updated_at=modified_time, created_at=createdtime, image=image, thumb_img=thumb_img)
              else:
                Place.objects.create(place_id=place_id, category=category[0], area_code=area_code2[0], title=title, address=address, map_x=map_x, map_y=map_y, tel=tel, updated_at=modified_time, created_at=createdtime, start_time=start_time, end_time=end_time, image=image, thumb_img=thumb_img)
      
      else:
        context['result'] = f'fail'
        context['error'] = 'category, areacode => Null'
        return JsonResponse(context)
      # 넣는 로직 필요함

      context['result'] = "success"
      context['data'] = data
  except Exception as e:
    context['result'] = f'fail'
    context['error'] = str(e)

  return JsonResponse(context)

def get_areacode(request):
  context = {}
  try:
    with transaction.atomic():
      data = api.get_all_areacode()

      AreaCode.objects.all().delete()

      for d in data:
        region_code = "{:02d}".format(int(d['code']))
        region_name = d['name']

        for c in d['childs']:
          area_code = f"{region_code}_{int(c['code']):02d}"
          name = c['name']

          AreaCode.objects.create(area_code=area_code, name=name, region_code=region_code, region_name=region_name)

      context['result'] = "success"
      context['data'] = data
  except Exception as e:
    context['result'] = 'fail'
    context['error'] = str(e)

  return JsonResponse(context)


def get_category(request):
  context  = {}
  try:
    with transaction.atomic():
      data = api.get_all_category(content_types=CONTANT_TYPE)

      Category.objects.all().delete()

      for d in data:
        category = d['category']
        content_type = d['content_type']
        name = d['name']
        Category.objects.create(category=category, content_type=content_type, name=name)

    context['result'] = "success"
    context['data'] = data
  except Exception as e:
    context['result'] = 'fail'
    context['error'] = str(e)
  return JsonResponse(context)