from django.shortcuts import render
from areacode.models import AreaCode

# Create your views here.
def index(request):
  area_codes = AreaCode.objects.all()

  return render(request, 'index.html', context={"area_codes": area_codes})
