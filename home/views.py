from django.shortcuts import render
from areacode.models import AreaCode
from place.models import Place
from django.utils import timezone

# Create your views here.
def index(request):
  today = timezone.now()
  area_codes = AreaCode.objects.all()
  events = Place.objects.filter(category__content_type=15, end_time__gt=today).order_by("end_time")[:10]

  return render(request, 'index.html', context={"area_codes": area_codes, "events": events, "today": today})
