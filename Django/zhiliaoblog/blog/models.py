from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


# Create your models here.


class BlogCategory(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = '博客分类'
        verbose_name_plural = verbose_name


class Blog(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    pub_time = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(BlogCategory, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = '博客'
        verbose_name_plural = verbose_name
        ordering = ['-pub_time']


class BlogComment(models.Model):
    content = models.TextField(verbose_name='内容')
    pub_time = models.DateTimeField(auto_now_add=True, verbose_name='发布时间')
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, verbose_name='引用博客', related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户')

    def __str__(self):
        return self.content

    class Meta:
        verbose_name = '博客评论'
        verbose_name_plural = verbose_name
        ordering = ['-pub_time']
