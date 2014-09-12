#coding=utf-8
from django import forms
from blog.models import Blog, Tag, Comments, Anybody
from django.contrib.auth.models import User
# from django.utils.translation import ugettext as _

from pagedown.widgets import PagedownWidget


class GiveoutForm(forms.Form):
    title = forms.CharField(label='标题', max_length=128,widget=forms.TextInput(attrs={'class':'form-control'}))
    # content = forms.CharField(label='内容', widget=forms.Textarea(attrs={'rows':10, 'cols':80, 'class':'form-control', 'id':'id_content'}))
    content = forms.CharField(
            label='内容',
            widget=PagedownWidget(show_preview=True, css=("css/demo1.css",), attrs={'class':' form-control'}),
            help_text='支持Markdown语法: <a href="http://wowubuntu.com/markdown/">语法说明</a>'
        )
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)   # 封装一组隐藏输入元素
    likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

    ## 取消关联
    # class Meta:
    #     model = Blog
    #     fields = ('title','content','views', 'likes')

    # def clean_username(self):
    #     username = self.cleaned_data['username']
    #     try:
    #         User.objects.get(username=username)
    #     except User.DoesNotExist:
    #         return username
    #     raise forms.ValidationError("User Name has been taken!")

class TagForm(forms.ModelForm):
    tag_name = forms.CharField(label='标签组', help_text="用逗号或空格分隔标签", widget=forms.TextInput(attrs={'class':'form-control'}))

    class Meta:
        model = Tag

    def clean(self):
        cleaned_data = self.cleaned_data
        tags = cleaned_data.get('tag_name', '')
        taglist = tags.replace(',',' ').split()
        cleaned_data['tag_name'] = taglist
        return cleaned_data

class CommentsForm(forms.ModelForm):
    comments = forms.CharField(
            label='评论',
            widget=PagedownWidget(show_preview=False, css=("css/demo2.css",)),
            help_text="限500字",
        )
    class Meta:
        model = Comments
        fields = ('comments',)

class AnybodyForm(forms.ModelForm):
    class Meta:
        model = Anybody