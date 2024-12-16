from django.shortcuts import render
from django.http import JsonResponse
from django.core.paginator import Paginator
from areacode.models import SigunguCode, AreaCode
from place.models import Place, Like
import logging
from collections import defaultdict
from datetime import datetime, timedelta
import os
from django.conf import settings
from django.shortcuts import get_object_or_404

logger = logging.getLogger(__name__)
from api import views

# Create your views here.
def local(request, areacode):
  # 해당 지역의 관광지 목록을 가져옴 (최신 4개)
  tour_list = Place.objects.all().filter(sigungu_code__area_code=areacode, category__content_type=12).order_by('-thumb_img', '-updated_at')[:4]
  
  # 해당 지역의 축제 목록을 가져옴 (최신 3개)
  event_list = Place.objects.all().filter(sigungu_code__area_code=areacode, category__content_type=15).order_by('-thumb_img', '-start_time')[:3]
  
  # 배너 이미지 목록을 생성
  # - local_[지역코드]_[1~3].jpg 형식의 이미지를 찾아서 목록에 추가
  # - 실제로 존재하는 이미지만 목록에 포함됨
  banner_images = []
  for i in range(1, 4):
      image_path = f'images/banners/local_{areacode}_{i}.jpg'
      if os.path.exists(os.path.join(settings.STATIC_ROOT or os.path.join(settings.BASE_DIR, 'static'), image_path)):
          banner_images.append(image_path)
  
  # 지역 코드에 해당하는 지역 이름을 데이터베이스에서 가져옴
  # (예: 1 → "서울", 4 → "대구")
  area_name = AreaCode.objects.get(area_code=areacode).name
  
  # 템플릿에 전달할 데이터를 context에 담음
  context = {
    'areacode': areacode,  # 지역 코드
    'area_name': area_name,  # 지역 이름 (예: "서울", "대구")
    'tour_list': tour_list,  # 관광지 목록
    'event_list': event_list,  # 축제 목록
    'banner_images': banner_images  # 배너 이미지 목록
  }
  
  # local.html 템플릿을 렌더링하여 응답
  return render(request, 'local.html', context)

view_counts = defaultdict(int)

from django.shortcuts import render

def view(request, areacode, content_id):
    context = {'around': '', 'len': 0}
    range_offset = 0.004
    content_data = Place.objects.filter(place_id=content_id)

    banner_images = []
    for i in range(1, 4):
        image_path = f'images/banners/local_{areacode}_{i}.jpg'
        if os.path.exists(os.path.join(settings.STATIC_ROOT or os.path.join(settings.BASE_DIR, 'static'), image_path)):
            banner_images.append(image_path)

    area_name = AreaCode.objects.get(area_code=areacode).name
    context['area_name'] = area_name
    context['banner_images'] = banner_images

    if content_data:
        # 주변 데이터 조회
        around_data = Place.objects.filter(
            sigungu_code__area_code=areacode,
            map_x__range=(float(content_data.map_x) - range_offset, float(content_data.map_x) + range_offset),
            map_y__range=(float(content_data.map_y) - range_offset, float(content_data.map_y) + range_offset)
        )

        if content_data.is_detail:
            context['result'] = "success"
            context['data'] = content_data
        else:
            try:
                context['result'] = 'info_success'
                context['data'] = views.get_info(contentid=content_id)
                if around_data.exists():
                    context['around'] = around_data
                    context['len'] = around_data.count()
            except Exception as e:
                print(e)
                return render(request, '404.html', status=404)

    # 좋아요 추가
    user = request.user
    if user.is_authenticated:
        like = Like.objects.filter(user=user, place=content_data[0])
        print(like)
        if like:
            context['like'] = True
        else:
            context['like'] = False
    else:
        context['like'] = False

    response = render(request, 'view.html', context)

    # 쿠키가 없었을 경우에만 새 쿠키 설정
    if cookie_name not in request.COOKIES:
        expires = datetime.now() + timedelta(hours=24)
        response.set_cookie(cookie_name, 'viewed', expires=expires)

    return response

def like_content(request, content_id):
    place = get_object_or_404(Place, place_id=content_id)
    user = request.user
    if user.is_authenticated:
        like, created = Like.objects.get_or_create(place=place, user=user)
        if not created:
            # 이미 좋아요를 눌렀다면 취소
            like.delete()
            return JsonResponse({'liked': False, 'like_count': place.like_count})

    return JsonResponse({'liked': True, 'like_count': place.like_count})

def local_list(request, areacode):
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    content_type = request.GET.get('content_type')
    
    # 배너 이미지 목록 생성
    banner_images = []
    for i in range(1, 4):
        image_path = f'images/banners/local_{areacode}_{i}.jpg'
        if os.path.exists(os.path.join(settings.STATIC_ROOT or os.path.join(settings.BASE_DIR, 'static'), image_path)):
            banner_images.append(image_path)
    
    # 이미지 우선순위를 위한 Case-When 구문
    from django.db.models import Case, When, Value, IntegerField
    image_priority = Case(
        When(thumb_img__isnull=False, thumb_img__gt='', then=Value(2)),
        When(thumb_img__isnull=True, image__isnull=False, image__gt='', then=Value(1)),
        When(thumb_img='', image__isnull=False, image__gt='', then=Value(1)),
        default=Value(0),
        output_field=IntegerField(),
    )
    
    # content_type에 따른 필터링
    if content_type == '15':  # 축제/행사
        places = Place.objects.filter(category__content_type=15)
    elif content_type == '12':  # 관광지
        places = Place.objects.filter(category__content_type__in=[12, 14, 25])
    else:
        # 기본값: 축제/행사
        places = Place.objects.filter(category__content_type=15)
    
    # 지역 코드로 필터링 및 정렬
    places = places.filter(sigungu_code__area_code=areacode)\
        .annotate(img_priority=image_priority)\
        .order_by('-img_priority', '-place_id')\
        .select_related('category', 'sigungu_code')
    
    if is_ajax:
        page = request.GET.get('page', 1)
        paginator = Paginator(places, 8)
        
        try:
            places_page = paginator.page(page)
        except (PageNotAnInteger, EmptyPage):
            places_page = paginator.page(1)
        
        places_data = []
        for place in places_page:
            # 이미지 URL 결정
            image_url = place.thumb_img or place.image or '/static/images/no-image.jpg'
            
            places_data.append({
                'place_id': place.place_id,
                'title': place.title,
                'thumb_img': image_url,
                'address': place.address or '',
                'start_time': place.start_time.strftime('%Y-%m-%d') if place.start_time else None,
                'end_time': place.end_time.strftime('%Y-%m-%d') if place.end_time else None,
            })
        
        return JsonResponse({
            'places': places_data,
            'has_next': places_page.has_next(),
            'next_page': places_page.next_page_number() if places_page.has_next() else None,
        })
    
    # 지역 이름 가져오기
    area_name = AreaCode.objects.get(area_code=areacode).name
    
    # 시군구 목록 가져오기
    sigungu_list = SigunguCode.objects.filter(area_code=areacode)
    
    # 초기 탭 설정
    initial_tab = request.GET.get('tab', 'event')
    
    return render(request, 'local_list.html', {
        'places': places,
        'areacode': areacode,
        'area_name': area_name,
        'banner_images': banner_images,
        'sigungu_list': sigungu_list,
        'initial_tab': initial_tab,
    })