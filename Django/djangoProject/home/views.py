from datetime import datetime

from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
def index(request):
    title = 'Django1111'
    title2 = {'title': 'Django2222', 'author': 'Django2222'}
    books = [
        {'title': 'Django1111', 'author': 'Django1111'},
        {'title': 'Django2222', 'author': 'Django2222'},
        {'title': 'Django3333', 'author': 'Django3333'},
    ]
    context = {'title': title, 'title2': title2, 'books': books}
    return render(request, 'index.html', context=context)


def if_view(request):
    age = 18
    return render(request, 'if.html', context={'age': age})


def for_view(request):
    books = [
        {'name': '三国策', 'author': '罗贯中'},
        {'name': '水浒传', 'author': '施耐庵'},
        {'name': '西游记', 'author': '吴承恩'},
        {'name': '红楼梦', 'author': '曹雪芹'},
    ]
    person = {'name': '张三', 'age': 18, 'sex': '男'}
    context = {
        'books': books,
        'person': person
    }

    return render(request, 'for.html', context=context)


def with_view(request):
    context = {
        'books':
            [
                {'name': '三国策', 'author': '罗贯中'},
                {'name': '水浒传', 'author': '施耐庵'},
                {'name': '西游记', 'author': '吴承恩'},
                {'name': '红楼梦', 'author': '曹雪芹'},
            ]
    }
    return render(request, 'with.html', context=context)


def url_view(request):
    return render(request, 'url.html')


def filter_view(request):
    great = "Hello World, this is great!"
    context = {
        'great': great,
        'birthday': datetime.now(),
        'profile': '',
    }
    return render(request, 'filter.html', context=context)


def new_index(request):
    context = {
        'articles': ['我的文章1', '我的文章2', '我的文章3']
    }
    return render(request, 'new_index.html', context=context)


def static_view(request):
    return render(request, 'static.html')
