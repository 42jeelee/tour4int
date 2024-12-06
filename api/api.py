import requests
from django.conf import settings

API_KEY = settings.API_KEY
API_BASE_URL = "http://apis.data.go.kr/B551011/KorService1"

BASE_PARAMS = {
  'serviceKey': API_KEY,
  'MobileOS': 'ETC',
  'MobileApp': 'AppTest',
  '_type': 'json',
}

def get_item(data, keys=[]):
  for k in keys:
    if not isinstance(data, dict):
      break

    data = data.get(k)
    
  if not isinstance(data, list):
    return []

  return data

def get_api_list(path, params={}, keys=[]):
  url = f"{API_BASE_URL}/{path}"
  params.update(BASE_PARAMS)

  res = requests.get(url, params=params)

  if res.status_code == 200:
    data = res.json()
    
    return get_item(data, keys)

  return []

def get_all_place(content_types=[]):
  path = "areaBasedList1"
  params = { 'numOfRows': 10000, 'pageNo': 1 }
  keys = ['response', 'body', 'items', 'item']

  data_list = []
  data_len = 1

  if len(content_types) > 0:
    for ct in content_types:
      params['contentTypeId'] = ct
      while data_len > 0:
        tmp = get_api_list(path, params, keys)
        data_len = len(tmp)
        data_list += tmp
        params['pageNo'] += 1
  else:
    while data_len > 0:
      tmp = get_api_list(path, params, keys)
      data_len = len(tmp)
      data_list += tmp
      params['pageNo'] += 1

  return data_list


def get_all_areacode():
  path = "areaCode1"
  params = { 'numOfRows': 50, 'pageNo': 1 }
  keys = ['response', 'body', 'items', 'item']

  return get_api_list(path, params, keys)

def get_all_sigungucode(area_code):
  path = "areaCode1"
  params = { 'numOfRows': 50, 'pageNo': 1, 'areaCode': area_code }
  keys = ['response', 'body', 'items', 'item']

  return get_api_list(path, params, keys)

def get_category(cat1=None, content_type=0):
  result = []
  path = "categoryCode1"
  params = { 'numOfRows': 50, 'pageNo': 1 }
  keys = ['response', 'body', 'items', 'item']
  
  if content_type != 0:
    params['contentTypeId'] = content_type
  
  if cat1 is None:
    data = get_api_list(path=path, params=params, keys=keys)

    result += get_category(cat1=data, content_type=content_type)
  else:
    for c in cat1:
      params['cat1'] = c['code']
      data = get_api_list(path=path, params=params, keys=keys)
      
      for d in data:
        d['content_type'] = content_type

      result += data
  
  return result



def get_all_category(cat1=None, content_types=[]):
  result = []

  if len(content_types) > 0:
    for ct in content_types:
      result += get_category(content_type=ct)

  return result



def get_event_info(datetime, pageNo=1, event=[]):
  path = "searchFestival1"
  params = {
      'numOfRows': 50,
      'pageNo': pageNo,
      'eventStartDate': datetime,
    }
  keys = ['response', 'body', 'items', 'item']
  data = get_api_list(path=path, params=params, keys=keys)
  for i in data:
    event.append(i)
  if len(event)  == len(data) * (pageNo):
    get_event_info(datetime=datetime, pageNo=pageNo+1, event=event)
  event_data = []
  for e_info in event:
    event_data.append({'contentid':e_info['contentid'], 'eventstartdate':e_info['eventstartdate'], 'eventenddate':e_info['eventenddate']})
  return event_data

def get_place_info(contentid):
  path = "detailCommon1"
  params = {
      'numOfRows': 1,
      'pageNo': 1,
      'defaultYN': 'Y',
      'defaultYN': 'Y',
      'overviewYN': 'Y',
      'contentId': contentid
    }
  keys = ['response', 'body', 'items', 'item']
  data = get_api_list(path=path, params=params, keys=keys)
  info = data[0]
  # return False
  return {'contentid':info['contentid'], 'homepage':info['homepage'], 'overview':info['overview']}