#coding=utf-8
from django.conf.urls import patterns, include, url

from django.views.generic import FormView
from django.conf.urls import patterns, url


urlpatterns = patterns('blog.views',
    url(r'^$', 'article_list'),
    url(r'^index/$', 'index', name = 'index'),
    url(r'^about/$', 'about', name = 'about'),

    url(r'^giveout/$', 'giveout', name = 'giveout'),
    url(r'^giveout/(?P<id>\d+)/$', 'giveout', name = 'giveout_edit'),
    url(r'^articles/$', 'article_list', name = 'article_list'),
    url(r'^articles/(?P<id>\d+)/$', 'article_show', name = 'article_show'),

    url(r'^login/$', 'user_login', name='user_login'),
    url(r'^logout/$', 'user_logout', name='user_logout'),

    # Search
    url(r'^tag_filter/(?P<id>\d+)/$', 'tag_filter', name = 'tag_filter'),
    url(r'^get_search/$', 'get_search', name = 'get_search'),

    # AJAX
    url(r'^like_article/$', 'like_article', name='like_article'),
    url(r'^comment_show/(?P<cmt_id>\d+)/$', 'comment_show', name='comment_show'),
    url(r'^reply_to_comt/(?P<reply_id>\d+)/$', 'reply_to_comt', name='reply_to_comt'),

    # Delete
    url(r'^del_article/(?P<id>\d+)/$', 'del_control', kwargs={'delconf':'article'}, name='del_article'),
    url(r'^del_comment/(?P<id>\d+)/$', 'del_control', kwargs={'delconf':'cmt'}, name='del_comment'),
    url(r'^del_reply/(?P<id>\d+)/$', 'del_control', kwargs={'delconf':'reply'}, name='del_reply'),
)

