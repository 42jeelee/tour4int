from django.http import JsonResponse
from django.shortcuts import render
from enum import Enum

class StaffOnlyMiddleware:

  class RESPONSE_TYPE(Enum):
    HTTPRESPONSE = 0
    APIRESPONSE = 1

  staff_urls = {
    '/touradmin': RESPONSE_TYPE.HTTPRESPONSE,
    '/api': RESPONSE_TYPE.APIRESPONSE,
  }

  def __init__(self, get_response):
    self.get_response = get_response
  
  def __call__(self, request):
    
    matched_url = next((url for url in self.staff_urls if request.path.startswith(url)), None)
    if matched_url is not None and not (request.user.is_superuser or request.user.is_staff):
      context = {"result": "fail", "error": "Permission denied! - 접근 권한이 없습니다."}
      return JsonResponse(context, status=403) \
        if self.staff_urls[matched_url] == self.RESPONSE_TYPE.APIRESPONSE \
        else render(request, '403.html', status=403)

    response = self.get_response(request)
    return response

