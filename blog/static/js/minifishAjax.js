$(document).ready(function() {
//当按钮被单击时, 触发URLconf映射, 调用 like_article 视图函数更新喜欢的类别, 并返回一个新喜欢数量. 当AJAX接收到响应 , 则更新相关文本和按钮
    $('#likes').click(function(){
        var catid;
        catid = $(this).attr("data-catid");
        $.get('/like_article/', {article_id:catid}, function(data){
            $('#like_count').html(data);
            $('#likes').hide();
        });
    });

});