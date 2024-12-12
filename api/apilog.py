from enum import Enum
from api.models import ApiFetchLog
from category.models import Category
from areacode.models import AreaCode, SigunguCode
from place.models import Place
from django.utils import timezone
from django.db.models import Q

class logType(Enum):
  EMPTY = 0
  CATEGORY = 1
  AREACODE = 2
  SIGUNGUCODE = 3
  PLACE = 4
  EVENT = 5

def trans_jsonformat(api_logger):
  return {
    'category': {
      'fetched': api_logger.is_category,
      'modify_date': api_logger.modify_category,
      'data_num': api_logger.category_num,
    },
    'areacode': {
      'fetched': api_logger.is_areacode,
      'modify_date': api_logger.modify_areacode,
      'data_num': api_logger.areacode_num,
    },
    'sigungucode': {
      'fetched': api_logger.is_sigungucode,
      'modify_date': api_logger.modify_sigungucode,
      'data_num': api_logger.sigungu_num,
    },
    'place': {
      'fetched': api_logger.is_place,
      'modify_date': api_logger.modify_place,
      'data_num': api_logger.place_num,
    },
    'event': {
      'fetched': api_logger.is_event,
      'modify_date': api_logger.modify_event,
      'data_num': api_logger.event_num,
    },
  }

def logging_fetch_log(fetchType=logType.EMPTY, context={}):
  if fetchType == logType.EMPTY or context['result'] != 'success':
    return
  
  api_logger = ApiFetchLog.objects.get(id=1)

  data_num = len(context.get('data', []))
  modify_num = context.get('modifed_count', 0)
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
  return logging_current()

def logging_current():
  api_logger = ApiFetchLog.objects.get(id=1)

  api_logger.category_num = Category.objects.count()
  api_logger.is_category = api_logger.category_num > 0
  if not api_logger.is_category: api_logger.modify_category = None
  
  api_logger.areacode_num = AreaCode.objects.count()
  api_logger.is_areacode = api_logger.areacode_num > 0
  if not api_logger.is_areacode: api_logger.modify_areacode = None
  
  api_logger.sigungu_num = SigunguCode.objects.count()
  api_logger.is_sigungucode = api_logger.sigungu_num > 0
  if not api_logger.is_sigungucode: api_logger.modify_sigungucode = None
  
  api_logger.place_num = Place.objects.filter(~Q(category__content_type=15)).count()
  api_logger.is_place = api_logger.place_num > 0
  if not api_logger.is_place: api_logger.modify_place = None
  
  api_logger.event_num = Place.objects.filter(category__content_type=15).count()
  api_logger.is_event = api_logger.event_num > 0
  if not api_logger.is_event: api_logger.modify_event = None

  api_logger.save()

  return trans_jsonformat(api_logger)


def has_fetch(logType=logType.EMPTY):
  api_logger = ApiFetchLog.objects.get(id=1)

  if logType == logType.CATEGORY: return api_logger.is_category
  if logType == logType.AREACODE: return api_logger.is_areacode
  if logType == logType.SIGUNGUCODE: return api_logger.is_sigungucode
  if logType == logType.PLACE: return api_logger.is_place
  if logType == logType.EVENT: return api_logger.is_event

  return False
  
def get_modify_time(fetchType=logType.EMPTY):
  api_logger = ApiFetchLog.objects.get(id=1)
  modified_time = timezone.now()

  if api_logger is not None:

    if fetchType == logType.CATEGORY and api_logger.modify_category is not None:
      modified_time =  api_logger.modify_category
    if fetchType == logType.AREACODE and api_logger.modify_areacode is not None:
      modified_time =  api_logger.modify_areacode
    if fetchType == logType.SIGUNGUCODE and api_logger.modify_sigungucode is not None:
      modified_time =  api_logger.modify_sigungucode
    if fetchType == logType.PLACE and api_logger.modify_place is not None:
      modified_time =  api_logger.modify_place
    if fetchType == logType.EVENT and api_logger.modify_event is not None:
      modified_time =  api_logger.modify_event

  return modified_time

def get_all_log():
  api_logger = ApiFetchLog.objects.get(id=1)

  return trans_jsonformat(api_logger)
