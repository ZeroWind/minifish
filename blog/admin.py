from django.contrib import admin
from blog.models import Blog, Tag



class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'createtime', 'modified', 'likes', 'views')
    search_fields = ['title']

admin.site.register(Blog, BlogAdmin)
admin.site.register(Tag)
