from django.db import models


# Create your models here.


class Auth(models.Model):
    name = models.CharField(max_length=20, verbose_name='作者名称')
    is_active = models.BooleanField(default=True, verbose_name='状态')

    def __str__(self):
        return self.name

    def delete(self, *args, **kwargs):
        self.is_active = False
        self.save()

        self.article_set.update(is_active=False)


class Article(models.Model):
    title = models.CharField(max_length=200, verbose_name='标题')
    content = models.TextField()
    pub_date = models.DateField()
    date_added = models.DateTimeField(auto_now_add=True)

    author = models.ForeignKey(Auth, on_delete=models.CASCADE, verbose_name='外键作者')
    is_active = models.BooleanField(default=True, verbose_name='状态')

    def __str__(self):
        return self.title[:30]
