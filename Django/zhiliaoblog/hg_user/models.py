from django.db import models
from django.contrib.auth.models import AbstractUser


class Organization(models.Model):
    org_id = models.CharField(max_length=20)
    org_name = models.CharField(max_length=200)
    org_desc = models.CharField(max_length=200)
    org_img = models.CharField(max_length=200)
    org_address = models.CharField(max_length=200)
    org_city = models.CharField(max_length=200)
    org_tel = models.CharField(max_length=200)
    is_primary = models.BooleanField()  # 是否是中心学校
    org_state = models.CharField(max_length=200)


class Dept(models.Model):
    dept_id = models.CharField(max_length=20)
    dept_name = models.CharField(max_length=200)
    dept_phone = models.CharField(max_length=200)
    dept_tel = models.CharField(max_length=200)
    dept_state = models.CharField(max_length=200)


class Position(models.Model):
    position_id = models.CharField(max_length=20)
    position_name = models.CharField(max_length=200)
    position_desc = models.CharField(max_length=200)
    position_state = models.CharField(max_length=200)


class CaptchaModel(models.Model):
    telephone = models.CharField(max_length=20, unique=True)
    captcha = models.CharField(max_length=4)
    create_time = models.DateTimeField(auto_now_add=True)


# Create your models here.
class HgUser(AbstractUser):
    username = models.CharField(max_length=20, unique=True)  # 登录名 j289103
    password = models.CharField(max_length=20, default='111111')  # 登录密码
    chinese_name = models.CharField(max_length=20)  # 夏燕
    id_card = models.CharField(max_length=20)  # 身份证号码
    sex = models.CharField(max_length=20)  # 这个根据身份证号码取
    # age = models.IntegerField()  # 这个根据身份证号码取
    birthday = models.DateField()  # 这个根据身份证号码取
    # job_date = models.DateField()  # 加入工作时间
    telephone = models.CharField(max_length=20)  # 手机号
    resume = models.CharField(max_length=500)  # 简介
    responsibility = models.CharField(max_length=500)  # 职责
    photo = models.CharField(max_length=200)  # 用户照片地址
    position_id = models.ForeignKey(Position, on_delete=models.CASCADE)  # 05，用户职务代码，对应有职务代码表。
    org_id = models.ForeignKey(Organization, on_delete=models.CASCADE)  # 14211280000 权限税务机关代码
    dept_id = models.ForeignKey(Dept, on_delete=models.CASCADE)  # 部门id,对应的是部门表 14211288100

    # user_state = models.BooleanField()  # 状态

    class Meta:
        unique_together = ('username', 'id_card', 'telephone')

    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        related_name='custom_user_set',
        help_text='The groups this user belongs to.',
        related_query_name='user'
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        related_name='custom_user_set',
        help_text='Specific permissions for this user.',
        related_query_name='user'
    )
