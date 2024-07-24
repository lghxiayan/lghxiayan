from django.http import HttpResponse
from django.shortcuts import render


def hello(request):
    return HttpResponse("Hello world ! ")


def runoob(request):
    context = {}
    context['hello'] = 'Hello World!'
    name = '菜鸟教程'
    views_name = '菜鸟教程'
    views_list = ['菜鸟教程', 'Google', 'Runoob', 'Taobao']
    views_dict = {'name': '菜鸟教程', 'url': 'www.runoob.com'}
    return render(request, 'runoob.html', {'name': name})
