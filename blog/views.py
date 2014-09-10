#coding=utf-8
from django.shortcuts import render_to_response, get_object_or_404, HttpResponse, RequestContext, HttpResponseRedirect
from blog.models import Tag, Blog, Anybody, Comments
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from blog.forms import GiveoutForm, TagForm, AnybodyForm, CommentsForm
from django.contrib.auth.models import User
from django.db.models import Q
import json

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
    ''' 意为竭力发表 or 编辑 '''
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

        else:
            print tags_form.errors, giveout_form.errors
        return HttpResponseRedirect(reverse('index'))

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


def article_show(request, id='', readviews=1):
    ''' Article detail Show'''
    context = RequestContext(request)
    context_dict = {}

    detail = get_object_or_404(Blog, pk=id)
    tags = detail.tags.all()

    views_count = 0
    views_count = detail.views + 1    # 阅读数, 未跟cookie绑定
    Blog.objects.filter(pk=id).update(views=views_count)

    # 上下页判断, 临时写法
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

    # 评论
    comment = comments_add(request, id)
    context_dict.update(comment)

    # 一堆字典..待整理
    context_dict['detail'] = detail
    context_dict['tags'] = tags
    context_dict['base_tags'] = get_tags()
    context_dict['base_views'] = get_views()
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
    if cat_id:
        articlelike = Blog.objects.get(id=int(cat_id))
        if articlelike:
            likes = articlelike.likes +1
            articlelike.likes = likes
            articlelike.save()
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
            print "Invalid login details: {0}, {1}".format(username, password)

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
    blog = get_object_or_404(Blog, pk=1)

    if request.method == 'POST':
        comment_form = CommentsForm(request.POST)
        anybody_form = AnybodyForm(request.POST)

        if comment_form.is_valid() and anybody_form.is_valid():
            comt = comment_form.save(commit=False)
            anyuser = anybody_form.cleaned_data

            try:
                # 邮箱存在不作记录, 仅更新访客名与站点
                email = Anybody.objects.get(email=anyuser['email'])
                if anyuser['website']:
                    Anybody.objects.filter(email=anyuser['email']).update(anyname=anyuser['anyname'],website=anyuser['website'])
            except:
                anybody_form.save()
                email = Anybody.objects.get(email=anyuser['email'])

            comt.email = email
            comt.save()

            comt.acticle_id.add(blog) # 麻烦的多对多..莫非还有更好的方法? ...待发现
            comt.save()
        else:
            print 'error!'

    comment_form = CommentsForm()
    anybody_form = AnybodyForm()

    # comments = blog.comments_set.all()
    comments = get_object_or_404(Blog,pk=id).comments_set.all()
    for comment in comments:
        anybody = Anybody.objects.filter(email=comment.email)[0]
        comment.name = anybody.anyname
        comment.website = anybody.website

    comments_count = comments.count()

    context_dict = {
        'comments_all':comments,
        'comment_form':comment_form,
        'anybody_form':anybody_form,
        'comments_count':comments_count
        }
    return context_dict


