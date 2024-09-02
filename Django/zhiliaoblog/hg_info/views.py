from django.http.response import JsonResponse
from django.shortcuts import render
from django.urls.base import reverse_lazy
from django.views.decorators.http import require_http_methods
from . import models
from . import forms
from django.http import HttpResponseBadRequest
from django.contrib.auth.decorators import login_required


# Create your views here.


def index(request):
    infos = models.Info.objects.all()
    return render(request, 'hg_index.html', context={'infos': infos})


def info_detail(request):
    pass


@require_http_methods(['GET', 'POST'])
@login_required(login_url=reverse_lazy('hg_user:login'))
def info_publish(request):
    if request.method == 'GET':
        infos = models.InfoCategory.objects.all()
        return render(request, 'hg_pub_info.html', context={'infos': infos})
    else:
        form = forms.PubInfoForm(request.POST)
        if form.is_valid():
            if 'content' in form.cleaned_data['content']:
                content = form.cleaned_data['content']
            else:
                return HttpResponseBadRequest('缺省必要的表单数据')
            title = form.cleaned_data['title']
            category_id = form.cleaned_data['category']
            print(category_id)
            info = models.Info.objects.create(title=title, content=content, category_id=category_id,
                                              author=request.user)
            return JsonResponse({'code': 200, 'msg': '信息发布成功', 'data': {'info_id': info.id}})
        else:
            print(form.errors)
            return HttpResponseBadRequest('表单数据无效')
            # return JsonResponse({'code': 400, 'msg': '信息发布失败!'})


def info_search(request):
    pass


def info_comment(request):
    pass
