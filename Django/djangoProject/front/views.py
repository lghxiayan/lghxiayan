from django.http import HttpResponse
from django.shortcuts import render
from django.db.models import Avg
from .models import Book, BookOrder, Publisher, Author
from .forms import MessageBoardForm, RegisterForm
from django.views.decorators.http import require_http_methods


# Create your views here.
def avg_view(request):
    result = Book.objects.aggregate(avg_price=Avg('price'))
    print(result)
    return HttpResponse('求平均值成功!')


@require_http_methods(['GET', 'POST'])
def index(request):
    if request.method == 'GET':
        form = MessageBoardForm()
        return render(request, 'front.html', context={'form': form})
    else:
        form = MessageBoardForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data.get('title')
            content = form.cleaned_data.get('content')
            email = form.cleaned_data.get('email')
            return HttpResponse(f'提交成功{title},{content},{email}')
        else:
            print(form.errors)
            return HttpResponse(form.errors)


@require_http_methods(['GET', 'POST'])
def register_view(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    else:
        form = RegisterForm(request.POST)
        if form.is_valid():
            telephone = form.cleaned_data.get('telephone')
            return HttpResponse(f"{telephone}")
        else:
            return HttpResponse(form.errors)
