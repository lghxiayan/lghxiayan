from django import forms
from django.contrib.auth.models import User

from hg_user.models import CaptchaModel


class LoginForm(forms.Form):
    username = forms.CharField(max_length=20, min_length=6)
    password = forms.CharField(max_length=20, min_length=6)
    remember_me = forms.IntegerField(required=False)


class RegisterForm(forms.Form):
    username = forms.CharField(max_length=20, min_length=6, error_messages={
        'required': '请输入用户名',
        'max_length': '用户名长度在6~20之间',
        'min_length': '用户名长度在6~20之间'
    })
    telephone = forms.CharField(max_length=20, error_messages={'required': '请输入手机号'})
    captcha = forms.CharField(max_length=20, error_messages={'required': '请输入手机验证码'})
    password = forms.CharField(max_length=20, min_length=6)

    def clean_username(self):
        username = self.cleaned_data.get('username')
        exists = User.objects.filter(username=username).exists()
        if exists:
            raise forms.ValidationError('用户名已经被注册')
        return username

    def clean_phone(self):
        telephone = self.cleaned_data.get('telephone')
        exists = User.objects.filter(telephone=telephone).exists()
        if exists:
            raise forms.ValidationError("手机号已经被注册")
        return telephone

    def clean_captcha(self):
        captcha = self.cleaned_data.get('captcha')
        telephone = self.cleaned_data.get('telephone')
        captcha_model = CaptchaModel.objects.filter(telephone=telephone, captcha=captcha).first()
        if not captcha_model:
            raise forms.ValidationError("验证码不匹配!")
        captcha_model.delete()
        return captcha
