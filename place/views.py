from django.shortcuts import render

# Create your views here.
def local(request, areacode):
  context = {'areacode': areacode}
  return render(request, 'local.html', context)


def view(request, areacode):
  context = {'areacode': areacode}
  return render(request, 'view.html', context)
  