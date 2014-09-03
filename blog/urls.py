#coding=utf-8
from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^index/$', 'blog.views.index', name = 'index'),
    url(r'^about/$', 'blog.views.about', name = 'about'),
    url(r'^giveout/$', 'blog.views.giveout', name = 'giveout'),
    url(r'^login/$', 'blog.views.user_login', name='user_login'),
)