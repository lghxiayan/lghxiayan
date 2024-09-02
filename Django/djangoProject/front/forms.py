from django import forms
from django.core import validators


class MessageBoardForm(forms.Form):
    title = forms.CharField(min_length=2, max_length=20, label='Title',
                            error_messages={
                                'min_length': '标题长度最小不能少于2',
                                'max_length': '标题最大不能大于20',
                            })
    content = forms.CharField(widget=forms.Textarea, label='标题内容')
    email = forms.EmailField(label='邮箱')


class RegisterForm(forms.Form):
    telephone = forms.CharField(
        validators=[validators.RegexValidator("1[345678]\d{9}", message="请输入正确格式的手机号码")])
