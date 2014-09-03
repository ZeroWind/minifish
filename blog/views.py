#coding=utf-8
from django.shortcuts import render_to_response, get_object_or_404, HttpResponse, RequestContext, HttpResponseRedirect
from blog.models import Tag, Blog, Profile
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from blog.forms import GiveoutForm, TagForm
from django.contrib.auth.models import User

# 主页
def index(request):
    context = RequestContext(request)
    ''' article 阅读排行'''

    title_list = Blog.objects.order_by('-views')[:10]
    context_dict = {'title_list':title_list}

    return render_to_response('blog/index.html', context_dict, context)

def giveout(request):
    context = RequestContext(request)
    ''' 竭力发表文章 '''
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('login')) #  kwargs={}

    if request.method == "POST":
        giveout_form = GiveoutForm(request.POST)
        tags_form = TagForm(request.POST)

        if giveout_form.is_valid() and tags_form.is_valid():
            giveout = giveout_form.cleaned_data
            tags = tags_form.cleaned_data
            print giveout['title'], tags['tag_name']

            user_ = User.objects.get(pk=1)
            print Profile(user=user_)
            blog = Blog(title = giveout['title'],
                    content = giveout['content'],
                    author = 'GreenFish',
                    views = giveout['views'],
                    likes = giveout['likes'],
                )
            blog.save()
            tag = Tag()
            for t in tags['tag_name']:
                Tag.objects.get_or_create(tag_name=t)

            for t in tags['tag_name']:
                blog.tags.add(Tag.objects.get(tag_name=t))
            blog.save()


        else:
            print tags_form.errors, giveout_form.errors
        return HttpResponseRedirect(reverse('index'))
    else:
        giveout_form = GiveoutForm()
        tags_form = TagForm()
    context_dict = {'giveout_form':giveout_form, 'tags_form':tags_form}
    return render_to_response('blog/giveout.html', context_dict, context)

def article_list(request):
    context = RequestContext(request)
    ''' article detail '''
    context_dict = {}
    return

def article_list(request):
    context = RequestContext(request)
    ''' article 分页 '''
    context_dict = {}
    return

def about(request):
    context = RequestContext(request)
    ''' about show '''
    context_dict = {}
    return

# 登录&注销
def user_login(request):
    context = RequestContext(request)
    ''' Login '''
    context_dict = {}
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)   # Django 内置验证

        if user:
            if user.is_active:
                login(request, user)                        # auto login
                return HttpResponseRedirect(reverse('index'))
            else:
                context_dict['disabled_account'] = True
                return render_to_response('blog/login.html', context_dict, context)
        else:
            print "Invalid login details: {0}, {1}".format(username, password)
            print context_dict
            context_dict['bad_details'] = True          # 控制模板显示的错误提示
            return render_to_response('blog/login.html', context_dict, context)
    else:
        return render_to_response('blog/login.html', context_dict, context)

@login_required()
def user_logout(request):
    ''' Logout '''
    logout(request)
    return HttpResponseRedirect(reverse('index'))



