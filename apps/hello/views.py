import json
import re
from django.shortcuts import render, get_object_or_404, render_to_response
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import ensure_csrf_cookie
from django.core.context_processors import csrf
from django.core.urlresolvers import reverse
from django.http import HttpResponse

from .models import MyData, StorageRequests
from .forms import EditDataForm


def home(request, pk='1'):
    obj = get_object_or_404(MyData, id=int(pk))
    return render(request, 'hello/home.html', {'obj': obj})


@ensure_csrf_cookie
def http_request_storage(request, symbol='+'):
    c = {}
    c.update(csrf(request))
    print symbol
    all_objs = StorageRequests.objects.all()
    if symbol == '-':
        objs = all_objs.order_by('-priority', )
    else:
        objs = all_objs
    data = objs.filter(viewed=False)
    context = {'objs': objs[:10], }

    if request.method == 'POST' and request.is_ajax():
        ids = []
        ids_str = json.loads(request.POST['ids_json'])
        pattern = '#(.+?): at'
        for i in ids_str:
            ids.append(int(re.search(pattern, i).group(1)))
        data.filter(id__in=ids).update(viewed=True)

        return render_to_response('hello/list_requests.html', context)

    return render(request, 'hello/storage_req.html', context)


@login_required
def edit_data(request, pk):
    data = MyData.objects.get(id=pk)
    response = {"success": False}
    if request.method == 'POST':
        form = EditDataForm(request.POST, request.FILES, instance=data)
        if form.is_valid() and request.is_ajax():
            form.save()
            response["success"] = True
            response['location'] = reverse('edit-data', kwargs={'pk': pk})
        else:
            response["errors"] = form.errors
        return HttpResponse(json.dumps(response),
                            mimetype="application/json")
    else:
        form = EditDataForm(instance=data)
    return render(request, 'hello/edit_data.html', {'form': form, 'pk': pk})
