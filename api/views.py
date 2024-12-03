from django.http import JsonResponse
from django.db import transaction
from areacode.models import AreaCode
from . import api

# Create your views here.
def get_place(request):
  return JsonResponse({"result": "empty"})

def get_areacode(request):
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
  except Exception as e:
    print("Exception:", e)

  return JsonResponse({"result": "success", "data": data})