from django.http import Http404, HttpResponse
from django.shortcuts import render

from article.models import Article, Auth


# Create your views here.


def index(request):
    return render(request, 'article/index.html')


def author(request):
    authors = Auth.objects.all()
    context = {'authors': authors}
    return render(request, 'article/auth.html', context=context)


def article_list(request, auth_id):
    # auth = Auth.objects.filter(id=auth_id)
    # author = auth[0]
    try:
        author = Auth.objects.get(id=auth_id)
    except Auth.DoesNotExist:
        return HttpResponse('没有这个人')
    articles = author.article_set.all()  # 这里是文章列表：<QuerySet [<Auth: 施耐庵>]>
    context = {'articles': articles, 'author': author}
    return render(request, 'article/article_list.html', context=context)
