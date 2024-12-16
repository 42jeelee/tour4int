from django.shortcuts import render
from django.db.models import Q, Count
from place.models import Place
from category.models import Category
from areacode.models import AreaCode

def search_view(request):
    query = request.GET.get('q', '')
    category_type = request.GET.getlist('type', [])
    area = request.GET.get('area', '')
    sort = request.GET.get('sort', 'latest')
    
    # 기본 쿼리셋
    places = Place.objects.select_related('category', 'sigungu_code').all()
    
    # 검색어 필터링
    if query:
        places = places.filter(
            Q(title__icontains=query) |
            Q(overview__icontains=query)
        )
    
    # 카테고리 필터링
    if category_type:
        places = places.filter(category__content_type__in=category_type)
    
    # 지역 필터링
    if area:
        places = places.filter(sigungu_code__area_code__code=area)
    
    # 정렬
    if sort == 'latest':
        places = places.order_by('-created_at')
    elif sort == 'popular':
        places = places.annotate(likes_count=Count('likes')).order_by('-likes_count')
    
    # 필터 옵션 데이터
    categories = Category.objects.all()
    areas = AreaCode.objects.all()
    
    context = {
        'places': places,
        'query': query,
        'categories': categories,
        'areas': areas,
        'selected_types': category_type,
        'selected_area': area,
        'sort': sort,
    }
    
    return render(request, 'search/search.html', context)
