from django.shortcuts import render
from django.db.models import Q, Count, Case, When, Value, BooleanField
from django.core.paginator import Paginator
from place.models import Place
from category.models import Category
from areacode.models import AreaCode

def search_view(request):
    query = request.GET.get('q', '')
    category_types = [ct for ct in request.GET.getlist('type', []) if ct]  # 빈 값 제거
    area_codes = [ac for ac in request.GET.getlist('area', []) if ac]  # 빈 값 제거
    sort = request.GET.get('sort', 'latest')
    page = request.GET.get('page', 1)
    
    # 기본 쿼리셋
    places = Place.objects.select_related('category', 'sigungu_code__area_code')
    
    # 검색어 필터링
    if query:
        places = places.filter(
            Q(title__icontains=query) |
            Q(overview__icontains=query)
        )
    
    # 카테고리 필터링
    selected_types = request.GET.getlist('type')
    if selected_types:
        category_conditions = Q()
        for type_value in selected_types:
            if type_value == 'tour':
                category_conditions |= Q(category__content_type__in=[12, 14, 25])
            elif type_value == 'event':
                category_conditions |= Q(category__content_type=15)
        if category_conditions:
            places = places.filter(category_conditions)
    
    # 지역 필터링
    if area_codes:
        # 쉼표로 구분된 문자열이 있을 경우 분리
        area_list = []
        for area_code in area_codes:
            if ',' in area_code:
                area_list.extend(area_code.split(','))
            else:
                area_list.append(area_code)
        places = places.filter(sigungu_code__area_code__area_code__in=area_list)
    
    # 썸네일 있는 글과 없는 글 구분
    places = places.annotate(
        has_thumbnail=Case(
            When(Q(thumb_img__isnull=False) & ~Q(thumb_img=''), then=Value(True)),
            When(Q(image__isnull=False) & ~Q(image=''), then=Value(True)),
            default=Value(False),
            output_field=BooleanField(),
        )
    )
    
    # 정렬
    if sort == 'popular':
        places = places.annotate(likes_count=Count('likes')).order_by('-has_thumbnail', '-likes_count', '-place_id')
    else:  # 기본값: latest
        places = places.order_by('-has_thumbnail', '-place_id')
    
    # 페이지네이션
    paginator = Paginator(places, 15)  # 페이지당 15개씩 표시
    page_obj = paginator.get_page(page)
    
    # 필터 옵션 데이터
    categories = [
        {'content_type': 'tour', 'name': '관광지'},
        {'content_type': 'event', 'name': '축제/행사'}
    ]
    areas = AreaCode.objects.all()
    
    # 선택된 필터 값들
    selected_areas = request.GET.getlist('area')
    
    # 배너 이미지 추가
    banner_images = ['images/banners/main_1.jpg', 'images/banners/main_2.jpg', 'images/banners/main_3.jpg']
    
    context = {
        'places': page_obj,
        'categories': categories,
        'areas': areas,
        'selected_types': selected_types,
        'selected_areas': selected_areas,
        'query': query,
        'sort': sort,
        'page_obj': page_obj,
        'banner_images': banner_images,  # 배너 이미지 추가
    }
    
    return render(request, 'search/search.html', context)
