from django.shortcuts import render
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.core.paginator import Paginator
from areacode.models import SigunguCode, AreaCode
from place.models import Place, Like, Views, Comment
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

from django.shortcuts import render
from .models import Place, Views  # Place와 Views 모델 import
import os
from django.conf import settings

from django.shortcuts import render
from .models import Place, Views  # Place와 Views 모델 import
import os
from django.conf import settings

def view(request, areacode, content_id):
    context = {'around': '', 'len': 0}
    range_offset = 0.004
    content_data = Place.objects.filter(place_id=content_id)

    # 배너 이미지 로드
    banner_images = []
    for i in range(1, 4):
        image_path = f'images/banners/local_{areacode}_{i}.jpg'
        if os.path.exists(os.path.join(settings.STATIC_ROOT or os.path.join(settings.BASE_DIR, 'static'), image_path)):
            banner_images.append(image_path)

    area_name = AreaCode.objects.get(area_code=areacode).name
    context['area_name'] = area_name
    context['banner_images'] = banner_images

    if len(content_data):  # 데이터가 존재하는 경우
        content_place = content_data.first()  # QuerySet에서 첫 번째 객체 가져오기
        views_record, created = Views.objects.get_or_create(place=content_place)  # 조회수 기록 가져오기 또는 생성하기

        # 현재 조회수를 컨텍스트에 추가
        context['view_count'] = views_record.count

        # 주변 데이터 로드
        around_data = Place.objects.filter(sigungu_code__area_code=areacode,
            map_x__gte=float(content_place.map_x) - range_offset,
            map_x__lte=float(content_place.map_x) + range_offset,
            map_y__gte=float(content_place.map_y) - range_offset,
            map_y__lte=float(content_place.map_y) + range_offset
        )
        context['around'] = around_data  # 주변 데이터를 컨텍스트에 추가

        if content_place.is_detail:
            context['result'] = "success"
            context['data'] = content_place
        else:
            try:
                context['result'] = 'info_success'
                context['data'] = views.get_info(contentid=content_id)
                if around_data:
                    context['around'] = around_data
                    context['len'] = len(around_data)
            except Exception as e:
                print(e)
                return render(request, '404.html', status=404)

    else:
        return render(request, '404.html', status=404)  # 데이터가 없는 경우 처리

    # 좋아요 추가
    user = request.user
    if user.is_authenticated:
        user.add_place_history(content_id)
        like = Like.objects.filter(user=user, place=content_place)
        context['like'] = like.exists()
    else:
        context['like'] = False

    # 표시할 필드와 레이블을 정의합니다
    fields_to_display = [
        ('chkbabycarriage', '유모차대여정보'),
        ('chkcreditcard', '신용카드가능정보'),
        ('chkpet', '애완동반가능정보'),
        ('expagerange', '체험가능연령'),
        ('expguide', '체험안내'),
        ('infocenter', '문의 및 안내'),
        ('opendate', '개장일'),
        ('parking', '주차시설'),
        ('restdate', '휴무일'),
        ('useseason', '이용시기'),
        ('usetime', '이용시간'),
        ('accomcountculture', '수용인원'),
        ('chkbabycarriageculture', '유모차대여정보'),
        ('chkcreditcardculture', '신용카드가능정보'),
        ('chkpetculture', '애완동반가능정보'),
        ('discountinfo', '할인정보'),
        ('infocenterculture', '문의 및 안내'),
        ('parkingculture', '주차시설'),
        ('parkingfee', '주차요금'),
        ('restdateculture', '휴무일'),
        ('usefee', '이용요금'),
        ('usetimeculture', '이용시간'),
        ('scale', '규모'),
        ('spendtime', '관람소요시간'),
        ('agelimit', '관람가능연령'),
        ('bookingplace', '예매처'),
        ('discountinfofestival', '할인정보'),
        ('eventstartdate', '행사시작일'),
        ('eventenddate', '행사종료일'),
        ('eventplace', '행사장소'),
        ('eventhomepage', '행사홈페이지'),
        ('festivalgrade', '축제등급'),
        ('placeinfo', '행사장 위치안내'),
        ('playtime', '공연시간'),
        ('program', '행사 프로그램'),
        ('spendtimefestival', '관람 소요시간'),
        ('sponsor1', '주최자 정보'),
        ('sponsor1tel', '주최자 연락처'),
        ('sponsor2', '주관사 정보'),
        ('sponsor2tel', '주관사 연락처'),
        ('subevent', '부대행사'),
        ('usetimefestival', '이용요금'),
        ('distance', '코스 총 거리'),
        ('infocentertourcourse', '문의 및 안내'),
        ('schedule', '코스 일정'),
        ('taketime', '코스 총 소요시간'),
        ('theme', '코스테마')
    ]

    display_fields = []
    for field, label in fields_to_display:
         value = getattr(context['data'], field, '') or getattr(context['data'], f"{field}culture", '')
         if value:
             value = value.replace('<br>', '')  
             display_fields.append((label, value))

    context['display_fields'] = display_fields

    # 덧글 불러오기
    comments = Comment.objects.filter(place=content_data[0]).order_by('-created_at')

    # 전체 댓글 개수
    total_comments = comments.count()

    # 각 필드의 'True' 값 비율 계산 (페이징 이전의 전체 댓글을 기준으로)
    if total_comments > 0:
        stats = {
            'stroller_rental': Comment.objects.filter(place=content_data[0], stroller_rental=True).count() / total_comments * 100,
            'credit_card': Comment.objects.filter(place=content_data[0], credit_card=True).count() / total_comments * 100,
            'pet_friendly': Comment.objects.filter(place=content_data[0], pet_friendly=True).count() / total_comments * 100,
            'parking': Comment.objects.filter(place=content_data[0], parking=True).count() / total_comments * 100,
            'restroom': Comment.objects.filter(place=content_data[0], restroom=True).count() / total_comments * 100,
            'elevator': Comment.objects.filter(place=content_data[0], elevator=True).count() / total_comments * 100,
            'wheelchair_path': Comment.objects.filter(place=content_data[0], wheelchair_path=True).count() / total_comments * 100,
            'wheelchair_rental': Comment.objects.filter(place=content_data[0], wheelchair_rental=True).count() / total_comments * 100,
        }
    else:
        stats = None

    context['stats'] = stats

    response = render(request, 'view.html', context)
    cookie_name = f'place_view_{content_id}'
    if cookie_name not in request.COOKIES:
        views_record.count += 1
        views_record.save()
        response.set_cookie(cookie_name, 'true', max_age=86400)
    return response



    

# testcode
def comment_list(request, place_id):
    place = get_object_or_404(Place, place_id=place_id)
    comments = Comment.objects.filter(place=place).order_by('-created_at')

    # 페이지네이션
    page_number = request.GET.get('page', 1)
    paginator = Paginator(comments, 5)  # 10개씩 페이지네이션

    try:
        page_obj = paginator.page(page_number)
    except:
        return JsonResponse({'error': 'Invalid page number'}, status=404)

    comment_data = [
        {
            'id': comment.id,
            'user': comment.user.nickname if comment.user else '삭제된 사용자',
            'content': comment.content,
            'created_at': comment.created_at.strftime('%Y-%m-%d %H:%M'),
        }
        for comment in page_obj.object_list
    ]

    return JsonResponse({
        'comments': comment_data,
        'has_next': page_obj.has_next(),
        'has_previous': page_obj.has_previous(),
        'page_number': page_obj.number,
        'total_pages': paginator.num_pages,
    })





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