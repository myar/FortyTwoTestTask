import json
from django.shortcuts import render, get_object_or_404, render_to_response

from apps.hello.models import MyData, StorageRequests


def home(request, pk='1'):
    obj = get_object_or_404(MyData, id=int(pk))
    return render(request, 'hello/home.html', {'obj': obj})


def http_request_storage(request):
    objs = StorageRequests.objects.all()
    data = objs.filter(viewed=False)
    context = {'objs': objs[:10],
               'count': data.count(),
               'new_ids': data.values_list('id', flat=True)}
    if request.is_ajax():
        if request.method == 'POST':
            ids = json.loads(request.POST['ids_json'])
            data.filter(id__in=ids).update(viewed=True)
            context['new_ids'] = data.values_list('id', flat=True)

        return render_to_response('hello/list_requests.html', context)
    return render(request, 'hello/storage_req.html', context)
