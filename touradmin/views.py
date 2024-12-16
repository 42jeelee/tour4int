from django.shortcuts import render
from place.models import Place
from accounts.models import User
from areacode.models import AreaCode, SigunguCode
from touradmin.models import BannerImage
from category.models import Category
from api import api
import os
from django.conf import settings
# Ajax
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from django.core import serializers # json타입 db에서 get으로 받을때
from django.core.files.storage import FileSystemStorage # 이미지 파일 관리
from django.shortcuts import get_object_or_404

# 이미지 경로지정 클레스
class StaticFileSystemStorage(FileSystemStorage):
    def __init__(self, *args, **kwargs):
        kwargs['location'] = os.path.join(settings.BASE_DIR, 'static', 'images', 'main-banners')
        kwargs['base_url'] = '/static/images/main-banners/'
        super().__init__(*args, **kwargs)

# 이미지 파일 업로드
def image_upload(request):
    if request.method == 'POST' and request.FILES['image']:
        uploaded_file = request.FILES['image']
        fs = StaticFileSystemStorage()
        file_name = fs.save(uploaded_file.name, uploaded_file)
        file_url = fs.url(file_name)

        # 이미지 경로를 딕셔너리 형태로 반환
        image_info = {
            "name": uploaded_file.name,
            "path": file_url
        }

        return JsonResponse({"success": True, "image": image_info})

    return JsonResponse({"success": False, "error": "파일 업로드 실패"})

# 이미지 삭제
def delete_image(request):
    banner_id = request.POST.get('bannerId')
    # 해당 배너 이미지 객체를 가져옵니다
    # banner = get_object_or_404(BannerImage, id=banner_id)

    # 이미지 파일 경로를 가져와 삭제합니다
    image_path = os.path.join(settings.BASE_DIR, 'static', banner_id)
    
    try:
        # 파일 삭제
        print(os.path.exists(image_path))
        if os.path.exists(image_path):
            print(image_path)
            os.remove(image_path)
        
        # 데이터베이스에서 배너 이미지 삭제
        # banner_id.delete()
        
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

# Create your views here.
def touradmin(request):
  image_dir = os.path.join(settings.STATIC_ROOT or os.path.join(settings.BASE_DIR, 'static'), 'images/main-banners')
  image_files = []

  if os.path.exists(image_dir):
    image_files = [
        {"name": file_name, "path": f'images/main-banners/{file_name}'}
        for file_name in os.listdir(image_dir)
        if file_name.lower().endswith(('.jpg', '.jpeg', '.png', '.gif'))
    ]

  context = {
    'users': User.objects.all(),
    'AreaCodes': AreaCode.objects.filter(),
    'events': Place.objects.filter(category__content_type = 15),
    'banners': image_files,
    'banners_active' : BannerImage.objects.all()
  }
  return render(request, 'touradmin.html', context)

# 각 지역별 관광지 데이터
def get_place(request):
  context = {}
  search = request.POST.get('areaCode')
  if search:
    area_data = Place.objects.filter(category__content_type = 12, sigungu_code__area_code__area_code = search)
    context['areaCode'] = list(area_data.values())
    context['result'] = 'success'
  else:
    context['result'] = 'fail'
  return JsonResponse(context)

# 각 지역별 이벤트 데이터
def get_event(request):
  context = {}
  search = request.POST.get('areaCode')
  if search:
    event_data = Place.objects.filter(category__content_type = 15, sigungu_code__area_code__area_code = search)
    context['event'] = list(event_data.values())
    context['result'] = 'success'
  else:
    context['result'] = 'fail'
  return JsonResponse(context)

# place 수정 타겟 데이터
def get_view(request):
  content = {}
  if request.method == 'POST':
    content_id = request.POST.get('no')
    content_data = Place.objects.get(place_id=content_id)
    if content_data.is_detail:
      content['result'] = "success"
      content['view'] = serializers.serialize('json', [content_data])
    else:
      overview = api.get_place_info(content_id)
      content_data.overview = overview['overview']
      content_data.homepage_url = overview['homepage']
      content_data.is_detail = True
      content_data.save()
      content['result'] = 'info_success'
      content['view'] = serializers.serialize('json', [content_data])
  else:
    content['result'] = 'fail'
  return JsonResponse(content)

# place 수정하기
def update(request):
  content = {}
  if request.method == 'POST':
    content_id = request.POST.get('target')
    title = request.POST.get('title')
    address = request.POST.get('address')
    image = request.POST.get('image')
    thumb_img = request.POST.get('thumb_img')
    homepage_url = request.POST.get('homepage_url')
    overview = request.POST.get('overview')
    data = Place.objects.get(place_id=content_id)
    data.title = title
    data.address = address
    data.image = image
    data.thumb_img = thumb_img
    data.homepage_url = homepage_url
    data.overview = overview
    data.save()
    content['result'] = 'success'
    content['view'] = serializers.serialize('json', [data])
  else:
    content['result'] = 'fail'
  return JsonResponse(content)

def get_user_view(request):
  content = {}
  if request.method == "POST":
    email = request.POST.get('email')
    user = User.objects.filter(email=email)
    content['result'] = 'success'
    content['view'] = serializers.serialize('json', [user[0]])
  return JsonResponse(content)

def update_user(request):
    content = {}
    if request.method == "POST":
        email = request.POST.get('email')
        name = request.POST.get('name')
        nickname = request.POST.get('nickname')
        address = request.POST.get('address')

        try:
            user = User.objects.get(email=email)
            user.name = name
            user.nickname = nickname
            user.address = address
            user.save()

            content['result'] = 'success'
            content['message'] = '회원정보가 성공적으로 수정되었습니다.'
            content['user'] = serializers.serialize('json', [user])
        except User.DoesNotExist:
            content['result'] = 'fail'
            content['message'] = '사용자를 찾을 수 없습니다.'
        except Exception as e:
            content['result'] = 'fail'
            content['message'] = str(e)
    else:
        content['result'] = 'fail'
        content['message'] = '잘못된 요청입니다.'
    return JsonResponse(content)
