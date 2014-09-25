#coding=utf-8
from django.shortcuts import render_to_response, get_object_or_404, HttpResponse, RequestContext, HttpResponseRedirect, render
from blog.models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from blog.forms import GiveoutForm, TagForm, AnybodyForm, CommentsForm
from django.contrib.auth.models import User
from django.db.models import Q
from django.template.loader import get_template
import json
from datetime import datetime

# mine
def index(request):
    ''' Article 阅读排行..等, 临时主页'''
    context = RequestContext(request)
    context_dict ={}

    title_list = Blog.objects.order_by('-views')[:5]
    if title_list:
        context_dict['title_list'] = title_list

    context_dict['base_tags'] = get_tags()
    context_dict['base_views'] = get_views()
    return render_to_response('blog/index.html', context_dict, context)


@login_required()
def giveout(request, id=''):
    ''' 发表 or 编辑 '''
    context = RequestContext(request)

    if request.method == "POST":
        giveout_form = GiveoutForm(request.POST)
        tags_form = TagForm(request.POST)

        if giveout_form.is_valid() and tags_form.is_valid():
            giveout = giveout_form.cleaned_data
            tags = tags_form.cleaned_data

            if id:
                blog = Blog.objects.get(id=id)
                blog.title = giveout['title']
                blog.content = content = giveout['content']
                blog.tags.clear()

            else:
                blog = Blog(title = giveout['title'],
                        content = giveout['content'],
                        author = User.objects.get(username=request.user.username),
                        views = giveout['views'],
                        likes = giveout['likes'],
                    )

            blog.save()

            # 存储
            for t in tags['tag_name']:
                Tag.objects.get_or_create(tag_name=t)

            for t in tags['tag_name']:
                blog.tags.add(Tag.objects.get(tag_name=t))
            blog.save()
            return HttpResponseRedirect(reverse('index'))
        else:
            print tags_form.errors, giveout_form.errors
    else:
        if id:
            # 编辑
            blog = get_object_or_404(Blog, pk=id)
            tags = blog.tags.all()
            giveout_form = GiveoutForm(initial={'title':blog.title, 'content':blog.content}, ) # auto_id=False
            tag_str_list = []
            for t in tags:
                tag_str_list.append(str(t))
            tag_str_list = ','.join(tag_str_list)
            tags_form = TagForm(initial={'tag_name':tag_str_list})

        else:
            giveout_form = GiveoutForm()
            tags_form = TagForm()

    context_dict = {'giveout_form':giveout_form, 'tags_form':tags_form}
    context_dict['base_tags'] = get_tags()
    context_dict['base_views'] = get_views()
    return render_to_response('blog/giveout.html', context_dict, context)


def article_show(request, id=''):
    ''' Article detail Show'''
    context = RequestContext(request)
    context_dict = {}

    detail = get_object_or_404(Blog, pk=id)
    tags = detail.tags.all()

    # sessions, 跟踪赞与阅读次数
    views_count = 0
    views = 'views_'+id
    if not request.session.get(views):
        request.session[views] = True
        views_count = detail.views + 1
        Blog.objects.filter(pk=id).update(views=views_count)

    if request.session.get('likes_'+id):
        context_dict['likes'] = True

    if request.session.get('reply_email'):
        context_dict['reply_user'] = request.session.get('reply_user')
        context_dict['reply_email'] = request.session.get('reply_email')

    # 上下页判断
    try:
        if Blog.objects.get(pk=int(id)+1):
            context_dict['previous_id'] = Blog.objects.get(pk=int(id)+1)
    except:
        context_dict['previous_id'] = None
    try:
        if Blog.objects.get(pk=int(id)-1):
            context_dict['next_id'] = Blog.objects.get(pk=int(id)-1)
    except:
        context_dict['next_id'] = None

    # 页面数据
    context_dict['tid'] = id
    context_dict['detail'] = detail
    context_dict['tags'] = tags
    context_dict['base_tags'] = get_tags()
    context_dict['base_views'] = get_views()

    # 评论
    comment = comments_add(request, id)
    context_dict.update(comment)

    return render_to_response('blog/article_show.html', context_dict, context)


def article_list(request):
    from django.core.paginator import Paginator
    from django.core.paginator import EmptyPage
    from django.core.paginator import PageNotAnInteger
    ''' article list '''
    context = RequestContext(request)
    context_dict = {}

    #  分页
    limit = 10
    arct_list = Blog.objects.all().order_by("-createtime")
    paginator = Paginator(arct_list, limit)

    page = request.GET.get('page')
    try:
        topics = paginator.page(page)
    except PageNotAnInteger:
        topics = paginator.page(1)
    except EmptyPage:
        topics = paginator.page(paginator.num_pages)

    context_dict['topics'] = topics
    context_dict['base_tags'] = get_tags()
    context_dict['base_views'] = get_views()
    return render_to_response('blog/articles.html',context_dict, context)

# other
def like_article(request):
    '''赞 Ajax'''
    context = RequestContext(request)
    cat_id = None
    if request.method == 'GET':
        cat_id = request.GET['article_id']
    likes = 0

    if request.session.get('likes') and request.session.get('like_id'):
        likes = Blog.objects.get(id=int(cat_id))
    else:
        if cat_id:
            articlelike = Blog.objects.get(id=int(cat_id))
            if articlelike:
                likes = articlelike.likes +1
                articlelike.likes = likes
                articlelike.save()
        request.session['likes_'+cat_id] = True

    return HttpResponse(likes)

def tag_filter(request, id=''):
    '''标签过滤页面'''
    context = RequestContext(request)

    tag = Tag.objects.get(id=id)
    blogs = tag.blog_set.all()

    context_dict = {'blogs':blogs}
    context_dict['base_tags'] = get_tags()
    context_dict['base_views'] = get_views()
    return render_to_response('blog/tag_filter.html', context_dict, context)

def get_tags(id=''):
    '''标签过滤侧边栏'''
    base_tags = Tag.objects.all()
    return base_tags

def get_views():
    '''点击排行侧边栏'''
    base_views = Blog.objects.order_by('-views')[:5]
    return base_views

def get_search(request):
    '''搜索'''
    context = RequestContext(request)
    context_dict = {}
    if 'search' in request.GET:
        srarch = request.GET['search']
        search_blogs = Blog.objects.filter(Q(content__icontains=srarch)|Q(title__icontains=srarch))

    context_dict['blogs'] = search_blogs
    context_dict['base_tags'] = get_tags()
    context_dict['base_views'] = get_views()
    return render_to_response('blog/tag_filter.html', context_dict, context)

def about(request):
    ''' About Show '''
    context = RequestContext(request)
    context_dict = {}
    context_dict['base_tags'] = get_tags()
    context_dict['base_views'] = get_views()
    return render_to_response('blog/about.html', context_dict, context)


# 登录&注销
def user_login(request):
    ''' Login '''
    context = RequestContext(request)
    context_dict = {}

    if 'next' in request.GET:
        next = request.GET['next']
    else:
        next = '/'

    context_dict['base_tags'] = get_tags()
    context_dict['base_views'] = get_views()
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)

                if request.POST['next']:
                    next = request.POST['next']         # 如果存在next, 否则为 '/'
                return HttpResponseRedirect(next,)
            else:
                context_dict['disabled_account'] = True
                return render_to_response('blog/login.html', context_dict, context)
        else:
            # print "Invalid login details: {0}, {1}".format(username, password)

            context_dict['bad_details'] = True
            return render_to_response('blog/login.html', context_dict, context)
    else:
        return render_to_response('blog/login.html', context_dict, context)

@login_required()
def user_logout(request):
    ''' Logout '''
    logout(request)
    return HttpResponseRedirect(reverse('index'))


# Comment Add and Show
def comments_add(request, id):
    '''评论'''
    context_dict = {}
    blog = get_object_or_404(Blog, pk=id)

    if request.method == 'POST' and request.is_ajax():
        comment_form = CommentsForm(request.POST)
        anybody_form = AnybodyForm(request.POST)

        if comment_form.is_valid() and anybody_form.is_valid():
            comt = comment_form.save(commit=False)
            anyuser = anybody_form.cleaned_data

            try:
                # 邮箱存在则不作记录, 仅更新访客名与站点
                email = Anybody.objects.get(email=anyuser['email'])
                if anyuser['website']:
                    Anybody.objects.filter(email=anyuser['email']).update(
                                                                    anyname=anyuser['anyname'],
                                                                    website=anyuser['website']
                                                                    )
            except:
                anybody_form.save()
                email = Anybody.objects.get(email=anyuser['email'])

            comt.email = email
            comt.save()

            comt.acticle_id.add(blog)
            comt.save()

            # 访客信息存入会话, 用于楼中楼
            request.session['reply_user'] = anyuser['anyname']
            request.session['reply_email'] = anyuser['email']

        else:
            # print 'error!', comment_form.errors, anybody_form.errors
            pass

    else:
        comment_form = CommentsForm()
        anybody_form = AnybodyForm()

    comments = blog.comments_set.all()
    for cmt in comments:
        anybody = Anybody.objects.filter(email=cmt.email)[0]
        cmt.name = anybody.anyname
        cmt.website = anybody.website
        cmt.reply = cmt.replyid.all()

    comments_count = comments.count()

    context_dict.update({
        'comments_all':comments,
        'comment_form':comment_form,
        'anybody_form':anybody_form,
        'comments_count':comments_count,
        })
    return context_dict

def comment_show(request, cmt_id):
    '''评论AJAX支持'''
    context_dict = {}
    cmt = comments_add(request, cmt_id)
    context_dict.update(cmt)

    if request.is_ajax():
        t = get_template('blog/comment_show.html')
        comment_html = RequestContext(request, context_dict)
    return HttpResponse(t.render(comment_html))


@login_required()
def del_control(request, delconf='', id=''):
    '''Delete Comment & Article & Reply'''
    if delconf=='cmt':
        cmt = get_object_or_404(Comments, pk=id)
        cmt.acticle_id.clear()
        reply =  cmt.replyid.all()
        reply.delete()
        cmt.delete()            # 删除评论
        return HttpResponseRedirect(request.META['HTTP_REFERER'])

    if delconf=='article':
        article = get_object_or_404(Blog, id=id)
        tags = article.tags.all()
        for tag in tags:
            tag_clear = tag.blog_set.all().count()
            if tag_clear <= 1:
                tag.delete()    # 清理标签
        article.tags.clear()    # 清理文章关系&删除文章
        article.delete()
        return HttpResponseRedirect('/articles/')

    if delconf=='reply':
        print id
        reply_comt = get_object_or_404(Replytocomt, pk=id)
        reply_comt.delete()     # 删除楼中楼评论
        return HttpResponseRedirect(request.META['HTTP_REFERER'])


# 回复.楼中楼
def reply_to_comt(request, reply_id):
    ''' 存有 Session 方可进行楼中楼的回复 '''
    if request.method == 'POST' and request.session.get('reply_email'):
        context_dict = {}
        reply_text = request.POST.get('text')

        # 储存
        comt = Comments.objects.filter(pk=reply_id)[0]
        anybody = Anybody.objects.filter(email=request.session.get('reply_email'))[0]

        reply = Replytocomt(replyuser=anybody, replytext=reply_text)
        reply.save()
        comt.replyid.add(reply.pk)

        context_dict['result'] = 'Create post successful!'
        context_dict['reply_id'] = reply_id
        context_dict['reply_pk'] = reply.pk
        context_dict['reply_text'] = reply.replytext
        context_dict['reply_user'] = reply.replyuser.anyname
        context_dict['reply_time'] = reply.createtime

        # t = get_template('blog/reply_show.html')
        # reply_html = RequestContext(request, context_dict)
        # return HttpResponse(t.render(reply_html))

    return HttpResponseRedirect(request.META['HTTP_REFERER'])
