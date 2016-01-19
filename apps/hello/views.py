import json
import re
from django.shortcuts import render, get_object_or_404, render_to_response

from django.views.decorators.csrf import ensure_csrf_cookie
from django.core.context_processors import csrf

from apps.hello.models import MyData, StorageRequests


def home(request, pk='1'):
    obj = get_object_or_404(MyData, id=int(pk))
    return render(request, 'hello/home.html', {'obj': obj})


@ensure_csrf_cookie
def http_request_storage(request):
    c = {}
    c.update(csrf(request))
    objs = StorageRequests.objects.all()
    data = objs.filter(viewed=False)
    new_ids = list(data.values_list('id', flat=True))
    context = {'objs': objs[:10],
               'count': data.count(),
               'new_ids': new_ids}

    if request.method == 'POST' and request.is_ajax():
        ids = []
        ids_str = json.loads(request.POST['ids_json'])
        pattern = '#(.+?): at'
        for i in ids_str:
            ids.append(int(re.search(pattern, i).group(1)))
        data.filter(id__in=ids).update(viewed=True)
        context['new_ids'] = list(data.values_list('id', flat=True))
        return render_to_response('hello/list_requests.html', context)

    return render(request, 'hello/storage_req.html', context)
