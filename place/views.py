from django.shortcuts import render
from place.models import Place

# Create your views here.
def local(request, areacode):
  tour_list = Place.objects.all().filter(sigungu_code__area_code=areacode, category__content_type=12)
  event_list = Place.objects.all().filter(sigungu_code__area_code=areacode, category__content_type=15)
  context = {
    'areacode': areacode,
    'tour_list': tour_list,
    'event_list': event_list
  }
  return render(request, 'local.html', context)


def view(request, areacode, content_id):
  context = {'areacode': areacode, 'place_id':content_id}
  return render(request, 'view.html', context)



def test(request):
  return render(request, 'test.html')
