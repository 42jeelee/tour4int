from django.shortcuts import render
from django.http import JsonResponse
from django.core.paginator import Paginator
from areacode.models import SigunguCode
from category.models import Category
from place.models import Place
import logging
from collections import defaultdict
from datetime import datetime, timedelta
import os
from django.conf import settings

logger = logging.getLogger(__name__)
from api import api

# Create your views here.
def local(request, areacode):
  tour_list = Place.objects.all().filter(sigungu_code__area_code=areacode, category__content_type=12).order_by('-thumb_img', '-updated_at')[:4]
  event_list = Place.objects.all().filter(sigungu_code__area_code=areacode, category__content_type=15).order_by('-thumb_img', '-start_time')[:3]
  
  # 실제 존재하는 배너 이미지만 리스트에 추가
  banner_images = []
  for i in range(1, 4):
      image_path = f'images/banners/local_{areacode}_{i}.jpg'
      if os.path.exists(os.path.join(settings.STATIC_ROOT or os.path.join(settings.BASE_DIR, 'static'), image_path)):
          banner_images.append(image_path)
  
  context = {
    'areacode': areacode,
    'tour_list': tour_list,
    'event_list': event_list,
    'banner_images': banner_images
  }
  return render(request, 'local.html', context)

view_counts = defaultdict(int)

def view(request, areacode, content_id):
    global view_counts
    context = {'around': '', 'len': 0}
    range_offset = 0.004
    content_data = Place.objects.filter(place_id=content_id)

    if len(content_data):
        # 조회수 관련 로직 추가
        cookie_name = f'place_view_{content_id}'
        
        # 쿠키가 없으면 조회수 증가
        if cookie_name not in request.COOKIES:
            view_counts[content_id] += 1

        # 현재 조회수를 컨텍스트에 추가
        context['view_count'] = view_counts[content_id]

        around_data = Place.objects.filter(sigungu_code__area_code=areacode,
            map_x__gte=float(content_data[0].map_x) - range_offset,
            map_x__lte=float(content_data[0].map_x) + range_offset,
            map_y__gte=float(content_data[0].map_y) - range_offset,
            map_y__lte=float(content_data[0].map_y) + range_offset
        )
        if content_data[0].is_detail:
            context['result'] = "success"
            context['data'] = content_data[0]
        else:
            overview = api.get_place_info(content_id)
            content_data[0].overview = overview['overview']
            content_data[0].homepage_url = overview['homepage']
            content_data[0].is_detail = True
            content_data[0].save()
            context['result'] = 'info_success'
            context['data'] = content_data[0]
        if around_data:
            context['around'] = around_data
            context['len'] = len(around_data)

    response = render(request, 'view.html', context)

    # 쿠키가 없었을 경우에만 새 쿠키 설정
    if cookie_name not in request.COOKIES:
        expires = datetime.now() + timedelta(hours=24)
        response.set_cookie(cookie_name, 'viewed', expires=expires)

    return response

def local_list(request, areacode):
  try:
      # 해당 지역의 시군구 코드 가져오기
      sigungu_list = SigunguCode.objects.filter(area_code=areacode)
      
      # AJAX 요청 여부 확인 (무한 스크롤을 위한 데이터 요청인지 확인)
      is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
      page = int(request.GET.get('page', 1))  # 현재 페이지 번호 (기본값: 1)
      content_type = request.GET.get('content_type', '15')  # 컨텐츠 타입 (기본값: 축제/행사)
      
      logger.debug(f"요청 처리 중: 지역코드={areacode}, 페이지={page}, 컨텐츠타입={content_type}")
      
      # 이미지 우선순위를 위한 Case-When 구문
      from django.db.models import Case, When, Value, IntegerField
      image_priority = Case(
          # 썸네일이 있는 경우 최우선
          When(thumb_img__isnull=False, thumb_img__gt='', then=Value(2)),
          # 썸네일은 없지만 이미지가 있는 경우
          When(thumb_img__isnull=True, image__isnull=False, image__gt='', then=Value(1)),
          When(thumb_img='', image__isnull=False, image__gt='', then=Value(1)),
          # 이미지가 전혀 없는 경우 후순위
          default=Value(0),
          output_field=IntegerField(),
      )
      
      # 컨텐츠 타입에 따라 장소 필터링
      if content_type == '15':
          # 축제/행사 (contentTypeId=15)
          places = Place.objects.filter(
              sigungu_code__area_code=areacode,
              category__content_type=15
          ).select_related('category', 'sigungu_code')
      else:
          # 관광지/문화시설/여행코스 (contentTypeId=12,14,25)
          places = Place.objects.filter(
              sigungu_code__area_code=areacode,
              category__content_type__in=[12, 14, 25]
          ).select_related('category', 'sigungu_code')
      
      # 이미지 우선순위에 따라 정렬
      places = places.annotate(
          img_priority=image_priority
      ).order_by('-img_priority', '-place_id')  # 이미지 우선순위로 정렬하고, 같은 우선순위 내에서는 최신순
      
      # 페이지네이션 (한 페이지당 8개 항목)
      paginator = Paginator(places, 8)
      page_obj = paginator.get_page(page)
      
      if is_ajax:
          # AJAX 요청일 경우 JSON 형태로 데이터 반환
          place_list = []
          for place in page_obj:
              try:
                  # 이미지 URL 결정 (우선순위: 썸네일 > 원본이미지 > 기본이미지)
                  image_url = place.thumb_img
                  if not image_url:
                      if place.image:
                          image_url = place.image
                      else:
                          image_url = '/static/images/no-image.jpg'
                  
                  # None 값 처리 (주소, 시작일, 종료일)
                  address = place.address if place.address else ''
                  start_time = place.start_time.strftime('%Y.%m.%d') if place.start_time else None
                  end_time = place.end_time.strftime('%Y.%m.%d') if place.end_time else None
                  
                  # 장소 데이터 구성
                  place_data = {
                      'title': str(place.title),
                      'thumb_img': str(image_url),
                      'address': str(address),
                      'start_time': start_time,
                      'end_time': end_time,
                  }
                  place_list.append(place_data)
              except Exception as e:
                  logger.error(f"장소 처리 중 오류 발생 {place.place_id}: {str(e)}")
                  continue
          
          # JSON 응답 데이터 구성
          response_data = {
              'places': place_list,  # 장소 목록
              'has_next': page_obj.has_next(),  # 다음 페이지 존재 여부
              'next_page': page + 1 if page_obj.has_next() else None,  # 다음 페이지 번호
          }
          logger.debug(f"응답 데이터: {response_data}")
          return JsonResponse(response_data)
      
      # 일반 요청일 경우 템플릿 렌더링
      # 실제 존재하는 배너 이미지만 리스트에 추가
      banner_images = []
      for i in range(1, 4):
          image_path = f'images/banners/local_{areacode}_{i}.jpg'
          if os.path.exists(os.path.join(settings.STATIC_ROOT or os.path.join(settings.BASE_DIR, 'static'), image_path)):
              banner_images.append(image_path)
      
      context = {
          'areacode': areacode,
          'banner_images': banner_images,
          'places': page_obj,
          'sigungu_list': sigungu_list,
      }
      return render(request, 'local_list.html', context)
      
  except Exception as e:
      logger.error(f"local_list 뷰 오류: {str(e)}", exc_info=True)
      if is_ajax:
          # AJAX 요청 중 오류 발생 시 에러 응답
          return JsonResponse({
              'error': str(e),
              'places': [],
              'has_next': False,
              'next_page': None,
          }, status=500)
      raise