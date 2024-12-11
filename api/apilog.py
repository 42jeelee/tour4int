from enum import Enum
from api.models import ApiFetchLog
from category.models import Category
from areacode.models import AreaCode, SigunguCode
from place.models import Place
from datetime import datetime
from django.utils import timezone
from django.db.models import Q

class logType(Enum):
  EMPTY = 0
  CATEGORY = 1
  AREACODE = 2
  SIGUNGUCODE = 3
  PLACE = 4
  EVENT = 5

def logging_fetch_log(fetchType=logType.EMPTY, context=0):
  if fetchType == logType.EMPTY or context['result'] != 'success':
    return
  
  api_logger = ApiFetchLog.objects.get(id=1)
  data_num = len(context['data'])
  modify_num = context['modifed_count']
  save_num = 0

  if fetchType == logType.CATEGORY:
    category_num = Category.objects.count()
    save_num = category_num
    
    api_logger.is_category = True
    api_logger.category_num = category_num
    api_logger.modify_category = timezone.now()
  elif fetchType == logType.AREACODE:
    areacode_num = AreaCode.objects.count()
    save_num = areacode_num

    api_logger.is_areacode = True
    api_logger.areacode_num = areacode_num
    api_logger.modify_areacode = timezone.now()
  elif fetchType == logType.SIGUNGUCODE:
    sigungucode_num = SigunguCode.objects.count()
    save_num = sigungucode_num

    api_logger.is_sigungucode = True
    api_logger.sigungu_num = sigungucode_num
    api_logger.modify_sigungucode = timezone.now()
  elif fetchType == logType.PLACE:
    place_num = Place.objects.filter(~Q(category__content_type=15)).count()
    save_num = place_num

    api_logger.is_place = True
    api_logger.place_num = place_num
    api_logger.modify_place = timezone.now()
  elif fetchType == logType.EVENT:
    event_num = Place.objects.filter(category__content_type=15).count()
    save_num = event_num

    api_logger.is_event = True
    api_logger.event_num = event_num
    api_logger.modify_event = timezone.now()
  
  api_logger.save()
  
  msg = f"💾 {fetchType.name} logging save [{modify_num}/{data_num}] current total [{save_num}]"
  print(msg)
  
def get_modify_time(fetchType=logType.PLACE):
  api_logger = ApiFetchLog.objects.get(id=1)

  modified_time = datetime.strptime('20210625', '%Y%m%d')

  if fetchType == logType.CATEGORY and  api_logger.modify_category is not None:
    modified_time =  api_logger.modify_category
  if fetchType == logType.AREACODE and  api_logger.modify_areacode is not None:
    modified_time =  api_logger.modify_areacode
  if fetchType == logType.SIGUNGUCODE and  api_logger.modify_sigungucode is not None:
    modified_time =  api_logger.modify_sigungucode
  if fetchType == logType.PLACE and  api_logger.modify_place is not None:
    modified_time =  api_logger.modify_place
  if fetchType == logType.EVENT and  api_logger.modify_event is not None:
    modified_time =  api_logger.modify_event

  return modified_time