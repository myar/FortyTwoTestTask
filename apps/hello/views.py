from django.shortcuts import render, get_object_or_404

from apps.hello.models import MyData


def home(request, pk='1'):
    obj = get_object_or_404(MyData, id=int(pk))
    return render(request, 'hello/home.html', {'obj': obj})
