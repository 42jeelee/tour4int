from django.http import JsonResponse

# Create your views here.
def all(request):
  return JsonResponse({"result": "empty"})