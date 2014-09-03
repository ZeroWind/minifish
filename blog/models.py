#coding=utf-8
from django.contrib.auth.models import User
from django.db import models


class Tag(models.Model):
    tag_name = models.CharField('标签',max_length=128, blank=True)

    def __unicode__(self):
        return self.tag_name

class Profile(models.Model):
    user = models.OneToOneField(User)

    def __unicode__(self):
        return self.user.get_full_name()

class Blog(models.Model):
    title = models.CharField('文章标题', max_length=128)
    author = models.CharField(max_length=50)
    content =models.TextField('内容')
    tags = models.ManyToManyField(Tag, blank=True)
    createtime = models.DateTimeField('发布日期', auto_now_add=True)
    modified = models.DateTimeField('修改时间', auto_now=True)
    likes = models.IntegerField(default=0)
    views = models.IntegerField(default=0)

    def __unicode__(self):
        return self.title + ' : ' + self.author

