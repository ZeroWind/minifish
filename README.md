#My Blog project

*第一个 Django(v1.6.2) 项目*

*基本功能完成, 剩下细节慢慢调整...*

*已部署 MiniFish Blog (o_O) Demo >>> http://minifish.pythonanywhere.com*

###当前实现

1. 登录 & 注销
2. 文章发布 & 编辑, 使用 pagedown & markdown_deux 
3. 文章列表, 分页, 标签云
4. Bootstrap 3 
5. 加入评论 & 点赞按钮, AJAX支持, 自己码评论, 未使用 Django 自带库
6. 简单的 Blog 管理, 删除博文及评论, 标签清理等

###待实现

评论楼中楼, 新浪微接入 API, 图片库 & 文件上传, 验证码, 访客行为跟踪 Session ..

###BUG:

bug#1描述: 评论表单[提交]请求后, 返回的响应被 AJAX 接收, 导致后端的表单数据验证提示无法渲染到页面

bug#1解决思路: 加入 AJAX前端验证, 恶补相关知识中...
 
###参考

《简易博客开发》不错的实例: http://www.cnblogs.com/cacique/tag/django/

心内求法《Django实战系列》: http://www.cnblogs.com/holbrook/archive/2012/03/02/2357343.html

Bootstrap 3: http://www.bootcss.com/

AJAX[浪潮之巅123]: http://www.cnblogs.com/xiaoqu/p/3224173.html

Django中国社区《五步教你实现使用Nginx+uWSGI+Django方法部署Django程序》: http://django-china.cn/