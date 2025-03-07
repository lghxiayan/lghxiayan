import random
from string import digits

from django.core.mail import send_mail

from django.http.response import JsonResponse
from django.shortcuts import render, redirect, reverse
from django.views.decorators.http import require_http_methods
from django.contrib.auth import get_user_model, login, logout, authenticate

from .forms import LoginForm, RegisterForm
from .models import CaptchaModel
from .utils import Message
from django.conf import settings

# Create your views here.
User = get_user_model()


def hg_index(request):
    return render(request, 'hg_index.html')


@require_http_methods(['GET', 'POST'])
def hg_login(request):
    if request.method == 'GET':
        return render(request, 'hg_login.html')
    else:
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            remember_me = form.cleaned_data.get('remember_me')
            # user = User.objects.filter(username=username).first()
            user = authenticate(username=username, password=password)
            if user and user.check_password(password):
                login(request, user)
                if not remember_me:
                    request.session.set_expiry(0)
            return redirect(reverse('hg_user:index'))
        else:
            print('用户名或密码错误')
            return redirect(reverse('hg_user:login'))


def hg_logout(request):
    # return render(request, 'hg_login.html')
    return redirect(reverse('hg_user:index'))


@require_http_methods(['GET', 'POST'])
def hg_register(request):
    if request.method == 'GET':
        return render(request, 'hg_register.html')
    else:
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            telephone = form.cleaned_data.get('telephone')

            user = User.objects.create_user(username=username, password=password, telephone=telephone)
            # user.telephone = form.cleaned_data.get('telephone')
            # user.save()

            return redirect(reverse('hg_user:login'))
        else:
            print(form.errors)
            return render(request, 'hg_register.html', {'form': form})


def send_phone_captcha(request):
    telephone = request.GET.get('telephone')
    if not telephone:
        return JsonResponse({'code': 400, 'msg': '必须输入手机号!'})
    captcha = "".join(random.sample(digits, 4))

    CaptchaModel.objects.update_or_create(telephone=telephone, defaults={'captcha': captcha})
    Message.send_sms(
        phone_numbers="13409790181",  # 测试手机号码
        sign_name=settings.ALIYUN_SIGN_NAME,  # 替换为你的短信签名
        template_code=settings.ALIYUN_TEMPLATE_CODE,  # 替换为你的短信模板ID
        template_param=f"{{'code':'{captcha}'}}"  # 替换为你的短信模板参数
    )

    return JsonResponse({'code': 200, 'msg': '手机验证码发送成功'})
