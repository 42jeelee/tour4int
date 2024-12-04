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

def get_api_list(path, params={}, keys=[], content_types=[]):
  url = f"{API_BASE_URL}/{path}"
  params.update(BASE_PARAMS)

  if len(content_types) > 0:
    result = []
    for ct in content_types:
      params['contentTypeId'] = ct

      res = requests.get(url, params=params)

      if res.status_code == 200:
        data = res.json()
        items = get_item(data, keys)

        if len(items) > 0:
          result.append(items)

    return result

  else:
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
  while data_len > 0:
    tmp = get_api_list(path, params, keys, content_types)
    data_len = len(tmp)
    data_list += tmp
    params['pageNo'] += 1

  return data_list


def get_all_areacode(area_code=None):
  result = []
  path = "areaCode1"
  params = { 'numOfRows': 20, 'pageNo': 1 }
  keys = ['response', 'body', 'items', 'item']

  if area_code is None:
    data_list = get_api_list(path, params, keys)

    for l in data_list:
      l['childs'] = get_all_areacode(l)
      result.append(l)
  else:
    params['areaCode'] = area_code['code']   
    
    result += get_api_list(path, params, keys)

  return result


