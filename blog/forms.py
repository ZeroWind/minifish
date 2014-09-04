#coding=utf-8
from django import forms
from blog.models import Blog, Tag
from django.contrib.auth.models import User

class GiveoutForm(forms.Form):
    title = forms.CharField(label='标题', max_length=128)
    content = forms.CharField(label='内容', widget=forms.Textarea)
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
    tag_name = forms.CharField(label='标签组', help_text="用逗号或空格分隔标签")

    class Meta:
        model = Tag

    def clean(self):
        cleaned_data = self.cleaned_data
        tags = cleaned_data.get('tag_name', '')
        taglist = tags.replace(',',' ').split()
        cleaned_data['tag_name'] = taglist
        return cleaned_data

