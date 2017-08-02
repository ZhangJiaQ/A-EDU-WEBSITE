from datetime import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class UserProfile(AbstractUser):
    nickname = models.CharField(max_length=20, default='', verbose_name='昵称')
    birday = models.DateField(null=True, blank=True, verbose_name='生日')
    gender = models.CharField(choices=(('male','nan'),('female','nv')),max_length=20, verbose_name='性别')
    address = models.CharField(max_length=20, default='', verbose_name='地址')
    mobile = models.CharField(max_length=11, null=True, blank=True, verbose_name='移动电话')
    image = models.ImageField(upload_to='image/%Y/%M',default='image/defaulty', verbose_name='头像')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.username


class EmailVerifyRecord(models.Model):
    code = models.CharField(max_length=20, verbose_name='验证码')
    email =models.EmailField(max_length=50, verbose_name='邮箱')
    send_type = models.CharField(choices=(('register','zhuce'),('forget','wangjimima')), verbose_name='验证码类型', max_length=12)
    send_time = models.DateTimeField(default=datetime.now, verbose_name='发送时间')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '邮箱验证码'
        verbose_name_plural = verbose_name

class PageBanner(models.Model):
    title = models.CharField(max_length=50, verbose_name='标题')
    image = models.ImageField(upload_to='bannar/%Y/%M' ,verbose_name='轮播图')
    url = models.URLField(max_length=200, verbose_name='访问地址')
    index = models.IntegerField(default=100, verbose_name='图片展示顺序')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加图片时间')

    class Meta:
        verbose_name = 'lunbotu'
        verbose_name_plural = verbose_name
