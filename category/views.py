from django.http import JsonResponse
from django.shortcuts import redirect
from api.api import *

# Create your views here.
def all(request):
  return JsonResponse({"result": "empty"})

def test(request):
  # for i in [12, 14, 15, 25]:
  #   get_all_category(contentid=i)
  return redirect('/')