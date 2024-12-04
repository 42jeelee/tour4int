import requests
from django.conf import settings
from category.models import Category

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

def get_all_category(cat1=None, content_types=[]):
  result = []
  num_of_rows = 50
  page_no = 1
  path = "categoryCode1"
  params = {
      'numOfRows': num_of_rows,
      'pageNo': page_no,
      'cat1': cat1,
    }
  keys = ['response', 'body', 'items', 'item']
  # 모든 Content_Type에 대한 cat1 데이터 추출
  if cat1 == None:
    cat1_data = get_api_list(path=path, params=params, keys=keys, content_types=content_types)
    result = get_all_category(cat1=cat1_data, content_types=content_types)
  else:
    # 해당 Content_Type에 대한 cat1값의 cat2값 분류
    for indx, two_list in enumerate(cat1):
      for data in two_list:
        params = {
          'numOfRows': num_of_rows,
          'pageNo': page_no,
          'cat1': data['code'],
        }
        # 분류된 cat2값 추출
        for i in get_api_list(path=path, params=params, keys=keys, content_types=[content_types[indx]]):
          for j in i:
            params = {
              'numOfRows': num_of_rows,
              'pageNo': page_no,
              'cat1': data['code'],
              'cat2': j['code'],
            }
            result.append({'content_type':content_types[indx], 'category':j['code'], 'name':j['name']})
    return result
  return result