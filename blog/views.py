#coding=utf-8
from django.shortcuts import render_to_response, get_object_or_404, HttpResponse, RequestContext, HttpResponseRedirect
from blog.models import Tag, Blog
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from blog.forms import GiveoutForm, TagForm
from django.contrib.auth.models import User

# mine
def index(request):
    ''' Article 阅读排行..等'''
    context = RequestContext(request)
    context_dict ={}

    title_list = Blog.objects.order_by('-views')[:10]
    if title_list:
        context_dict['title_list'] = title_list

    context_dict['base_tags'] = get_tags()
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
            giveout_form = GiveoutForm(initial={'title':blog.title, 'content':blog.content}, auto_id=False)
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
    return render_to_response('blog/giveout.html', context_dict, context)


def article_show(request, id=''):
    ''' Article detail Show'''
    context = RequestContext(request)
    context_dict = {}

    detail = get_object_or_404(Blog, pk=id)
    tags = detail.tags.all()

    context_dict['detail'] = detail
    context_dict['tags'] = tags
    context_dict['base_tags'] = get_tags()
    return render_to_response('blog/article_show.html', context_dict, context)


def article_list(request):
    from django.core.paginator import Paginator
    from django.core.paginator import EmptyPage
    from django.core.paginator import PageNotAnInteger
    ''' article list '''
    context = RequestContext(request)
    context_dict = {}

    #  分页
    limit = 5
    arct = Blog.objects.all()
    paginator = Paginator(arct, limit)

    page = request.GET.get('page')
    try:
        topics = paginator.page(page)
    except PageNotAnInteger:
        topics = paginator.page(1)
    except EmptyPage:
        topics = paginator.page(paginator.num_pages)

    context_dict['topics'] = topics
    context_dict['base_tags'] = get_tags()
    return render_to_response('blog/articles.html',context_dict, context)

# other
def tag_filter(request, id=''):
    '''标签过滤页面'''
    context = RequestContext(request)

    tag = Tag.objects.get(id=id)
    blogs = tag.blog_set.all()

    context_dict = {'blogs':blogs, 'tag':tag}
    context_dict['base_tags'] = get_tags()
    return render_to_response('blog/tag_filter.html', context_dict, context)

def get_tags(id=''):
    '''标签过滤侧边栏'''
    base_tags = Tag.objects.all()
    return base_tags

def about(request):
    ''' About Show '''
    context = RequestContext(request)
    context_dict = {}
    context_dict['base_tags'] = get_tags()
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



