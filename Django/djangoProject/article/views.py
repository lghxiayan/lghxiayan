from datetime import datetime

from django.shortcuts import render, HttpResponse
from .models import User, Article


# Create your views here.


def add_article(request):
    user = User(username='张三', password='123456')
    user.save()

    article = Article(author=user, title="标题", content="内容")
    article.save()
    # article = Article.objects.first()
    # print(article.author.username)
    return HttpResponse(f"add_article成功{article.author.username}")


def one_to_many(request):
    user = User.objects.first()
    # print(user)
    articles = user.article_set.all()
    # print(articles)
    retStr = ''
    for article in articles:
        # print(article.title)
        retStr += f"{article.title}: {article.content} | "
        print(f"Article: {article.title}")  # 添加这条打印语句
        print(retStr)
    retStr += '<br>'
    print(retStr)
    return HttpResponse(f"sucessed!{retStr}")


def query_1(request):
    article = Article.objects.filter(id__exact=7)
    # print(article.title, article.content)
    print(article, type(article))
    print(article.query)
    for a in article:
        print(a.title)
    return HttpResponse("查询成功")


def query_4(request):
    start_date = datetime(year=2024, month=1, day=1)
    end_date = datetime(year=2024, month=8, day=30)
    articles = Article.objects.filter(pub_time__range=(start_date, end_date))
    print(articles)
    print(articles.count())
    print(articles.query)
    return HttpResponse("日期范围查询成功")
