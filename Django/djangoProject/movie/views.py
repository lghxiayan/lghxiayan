from django.shortcuts import render, HttpResponse


# Create your views here.


def movie_list(request):
    return HttpResponse('电影列表：movie_list')


def movie_detail(request, movie_id):
    return HttpResponse(f'电影详情：movie_detail, {movie_id}')
