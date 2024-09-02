import string

from django.shortcuts import render, redirect, reverse
from django.http.response import JsonResponse
from string import digits
import random
from django.core.mail import send_mail
from .models import CaptchaModel
from django.views.decorators.http import require_http_methods
from .forms import ResisterForm, LoginForm
from django.contrib.auth import get_user_model, login, logout

User = get_user_model()


# Create your views here.


@require_http_methods(['GET', 'POST'])
def zllogin(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            remember = form.cleaned_data.get('remember')
            user = User.objects.filter(email=email).first()
            if user and user.check_password(password):
                login(request, user)
                if not remember:
                    request.session.set_expiry(0)
            return redirect('/')
        else:
            print('邮箱或密码错误')
            # form.add_error('email', '邮箱或密码错误')
            # return render(request, 'login.html', context={'form': form})
            return redirect(reverse('zlauth:login'))


def zllogout(request):
    logout(request)
    return redirect('/')


@require_http_methods(['GET', 'POST'])
def register(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    else:
        form = ResisterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            User.objects.create_user(username=username, email=email, password=password)
            return redirect(reverse('zlauth:login'))
        else:
            print(form.errors)
            # return redirect(reverse('zlauth:register'))
            return render(request, 'register.html', {'form': form})


def send_email_captcha(request):
    email = request.GET.get('email')
    if not email:
        return JsonResponse({'code': 400, 'msg': '必须传递邮箱！'})
    captcha = "".join(random.sample(digits, 4))
    CaptchaModel.objects.update_or_create(email=email, defaults={'captcha': captcha})
    send_mail(subject='注册验证码', message=f"你的注册验证码是: {captcha}", recipient_list=[email], from_email=None)
    return JsonResponse({'code': 200, 'msg': '邮箱验证码发送成功！'})


def index_view(request):
    return render(request, 'index.html')
