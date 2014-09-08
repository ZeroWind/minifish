#coding=utf-8
from django.conf.urls import patterns, include, url

from django.views.generic import FormView
from django.conf.urls import patterns, url


urlpatterns = patterns('',
    url(r'^$', 'blog.views.index'),
    url(r'^index/$', 'blog.views.index', name = 'index'),
    url(r'^about/$', 'blog.views.about', name = 'about'),

    url(r'^giveout/$', 'blog.views.giveout', name = 'giveout'),
    url(r'^giveout/(?P<id>\d+)/$', 'blog.views.giveout', name = 'giveout_edit'),
    url(r'^articles/$', 'blog.views.article_list', name = 'article_list'),
    url(r'^articles/(?P<id>\d+)/$', 'blog.views.article_show', name = 'article_show'),

    # srarch
    url(r'^tag_filter/(?P<id>\d+)/$', 'blog.views.tag_filter', name = 'tag_filter'),
    url(r'^get_search/$', 'blog.views.get_search', name = 'get_search'),

    url(r'^login/$', 'blog.views.user_login', name='user_login'),
    url(r'^logout/$', 'blog.views.user_logout', name='user_logout'),

    #AJAX
    url(r'^like_article/$', 'blog.views.like_article', name='like_article'),
)

