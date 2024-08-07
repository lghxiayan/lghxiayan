from django.shortcuts import render, HttpResponse
from django.db import connection
from .models import Book


# Create your views here.

def index(request):
    cursor = connection.cursor()
    cursor.execute("select * from book_book")
    rows = cursor.fetchall()
    for row in rows:
        print(row)
    return HttpResponse(f"Hello World {rows}")


def add_book(request):
    # book = Book(name="红楼梦", author="曹雪芹", pub_time="1980-01-01", price=100)
    book = Book(name="三国演义", author="罗贯中", )
    book.save()
    return HttpResponse("添加成功")


def query_book(request):
    book = Book.objects.get(author="曹雪芹")
    # for book in books:
    if book:
        print(book.id, book.name, book.author, book.pub_time, book.price)
    return HttpResponse("查询成功")


def order_book(request):
    books = Book.objects.order_by("price")
    for book in books:
        print(book.id, book.name, book.author, book.pub_time, book.price)
    return HttpResponse("排序成功")


def update_book(request):
    try:
        book = Book.objects.get(author="曹雪芹")
        book.name = '阿里巴巴'
        book.save()
    except Book.DoesNotExist:
        return HttpResponse("更新失败")
    return HttpResponse("更新成功")


def delete_book(request):
    try:
        book = Book.objects.filter(author="曹雪芹")
        book.delete()
    except Book.DoesNotExist:
        return HttpResponse("删除失败")
    return HttpResponse("删除成功")


def add_article(request):
    article = Article(title="abc", content="abc")
    author = User(username='张三', password='123')
    Article.author = author
    article.save()


def book_detail_query_string(request):
    book_id = request.GET.get('id')
    return HttpResponse(f"你要查询的图书id是：{book_id},函数名称：book_detail_query_string")


def book_detail_path(request, book_id):
    return HttpResponse(f"你要查询的图书id是：{book_id}")
