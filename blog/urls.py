#coding=utf-8
from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'blog.views.index'),
    url(r'^index/$', 'blog.views.index', name = 'index'),
    url(r'^about/$', 'blog.views.about', name = 'about'),

    url(r'^giveout/$', 'blog.views.giveout', name = 'giveout'),
    url(r'^giveout/(?P<id>\d+)/$', 'blog.views.giveout', name = 'giveout_edit'),
    url(r'^articles/$', 'blog.views.article_list', name = 'article_list'),
    url(r'^articles/(?P<id>\d+)/$', 'blog.views.article_show', name = 'article_show'),
    url(r'^tag_filter/(?P<id>\d+)/$', 'blog.views.tag_filter', name = 'tag_filter'),
    # url(r'^articles_edit/(?P<id>\d+)/$', 'blog.views.article_edit', name = 'article_edit'),

    url(r'^login/$', 'blog.views.user_login', name='user_login'),
    url(r'^logout/$', 'blog.views.user_logout', name='user_logout'),
)