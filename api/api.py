import requests
from django.conf import settings

API_KEY = settings.API_KEY
API_BASE_URL = "http://apis.data.go.kr/B551011/KorService1"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
}

def get_all_place():
  num_of_rows = 10
  page_no = 1
  area_code = 1

  url = f"{API_BASE_URL}/areaBasedList1?MobileOS=ETC&MobileApp=AppTest\
            &_type=json&numOfRows={num_of_rows}&pageNo={page_no}\
            &areaCode={area_code}&serviceKey={API_KEY}"

  print(url)


def get_all_areacode(area_code=None):
  result = []
  num_of_rows = 20
  page_no = 1
  params = {
    'serviceKey': API_KEY,
    'numOfRows': num_of_rows,
    'pageNo': page_no,
    'MobileOS': 'ETC',
    'MobileApp': 'AppTest',
    '_type': 'json',
  }

  if area_code is None:
    url = f"{API_BASE_URL}/areaCode1?serviceKey={API_KEY}&numOfRows={num_of_rows}&pageNo={page_no}\
            &MobileOS=ETC&MobileApp=AppTest&_type=json"
    
    res = requests.get(url, params=params)

    if res.status_code == 200:
      data = res.json()
      items = data['response']['body']['items']['item']

      for item in items:
        item['childs'] = get_all_areacode(item)
        result.append(item)
  else:
    url = f"{API_BASE_URL}/areaCode1?serviceKey={API_KEY}&numOfRows={num_of_rows}&pageNo={page_no}\
            &MobileOS=ETC&MobileApp=AppTest&_type=json&areaCode={area_code['code']}"
    
    res = requests.get(url, params=params)

    if res.status_code == 200:
      data = res.json()
      
      items = data['response']['body']['items']['item']

      for item in items:
        result.append(item)

  return result


