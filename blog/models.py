#coding=utf-8
from django.contrib.auth.models import User
from django.db import models


class Tag(models.Model):
    tag_name = models.CharField('标签',max_length=128, blank=True)

    def __unicode__(self):
        return self.tag_name

class Blog(models.Model):
    title = models.CharField('文章标题', max_length=128)
    author = models.ForeignKey(User)
    content =models.TextField('内容')
    tags = models.ManyToManyField(Tag, blank=True)
    createtime = models.DateTimeField('发布日期', auto_now_add=True)
    modified = models.DateTimeField('修改时间', auto_now=True)
    likes = models.IntegerField(default=0)
    views = models.IntegerField(default=0)

    class Meta:
        ordering = ['-modified']

    def __unicode__(self):
        return self.title



class Anybody(models.Model):
    anyname = models.CharField('访客', max_length=64)
    email = models.EmailField('Email')
    website = models.CharField('站点', max_length=258, blank=True, null=True)
    createtime = models.DateTimeField('用户创建日期', auto_now_add=True)
    updatetime = models.DateTimeField('更新日期', auto_now=True)

    def __unicode__(self):
        return self.email

class Comments(models.Model):
    acticle_id = models.ManyToManyField(Blog)
    email = models.ForeignKey(Anybody)
    comments = models.TextField('评论', max_length=500)
    commentstime = models.DateTimeField('评论日期', auto_now_add=True)
    updatetime = models.DateTimeField('更新日期', auto_now=True)

    class Meta:
        ordering = ['commentstime']

    def __unicode__(self):
        return self.comments

