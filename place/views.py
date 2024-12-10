from django.shortcuts import render
from areacode.models import SigunguCode
from category.models import Category
from place.models import Place

# Create your views here.
def local(request, areacode):
  context = {'areacode': areacode}
  return render(request, 'local.html', context)


def view(request, areacode, content_id):
  context = {'areacode': areacode, 'place_id':content_id}
  return render(request, 'view.html', context)



def test(request):
  return render(request, 'test.html')
