from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.
User = get_user_model()


class InfoCategory(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = '信息分类'
        verbose_name_plural = verbose_name


class Info(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    pub_time = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(InfoCategory, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)


class InfoComment(models.Model):
    content = models.TextField()
    pub_time = models.DateTimeField(auto_now_add=True)
    info = models.ForeignKey(Info, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    # 这个暂时不用,跟blog有点区别.先观察,出错再启用.
    def __str__(self):
        return self.content
