from django.shortcuts import render, get_object_or_404

from apps.hello.models import MyData, StorageRequests


def home(request, pk='1'):
    obj = get_object_or_404(MyData, id=int(pk))
    return render(request, 'hello/home.html', {'obj': obj})


def http_request_storage(request):
    objs = StorageRequests.objects.all().order_by('req_date')[:10]
    return render(request, 'hello/storage_req.html', {'objs': objs, })
