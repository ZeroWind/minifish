$(document).ready(function() {
    //当按钮被单击时, 触发URLconf映射, 调用 like_article 视图函数更新喜欢的类别, 并返回一个新喜欢数量. 当AJAX接收到响应 , 则更新相关文本和按钮
    $('#likes').click(function(){
        var catid;
        catid = $(this).attr("data-catid");
        $.get('/like_article/', {article_id:catid}, function(data){
            $('#like_count').html(data);
            $('#likes').hide();
        });
        $("#showlike").html('<button class="btn btn-xs btn-success" type="button" disabled="disabled">已赞</button>');
    });

    $("textarea").addClass(" form-control");
    $("#comment_form input").addClass(" form-control").css({
        width:"50%",
    });

    bindPostCommentHandler(); // 评论AJAX
});




$(document).ajaxSend(function(event, xhr, settings) {
    // 用jQuery来处理ajax解决csrftoken问题--每次提交时处理cookie的过程
    // 该函数获取给定名称的cookie
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    //检查地址是否来自相同来源
    function sameOrigin(url) {
        // url could be relative or scheme relative or absolute
        var host = document.location.host; // host + port
        var protocol = document.location.protocol;
        var sr_origin = '//' + host;
        var origin = protocol + sr_origin;
        // Allow absolute or scheme relative URLs to same origin
        return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
            (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
            // or any other URL that isn't scheme relative or absolute i.e relative.
            !(/^(\/\/|http:|https:).*/.test(url));
    }
    function safeMethod(method) {
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    // 用jQuery来处理ajax解决csrftoken问题
    if (!safeMethod(settings.type) && sameOrigin(settings.url)) {
        xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
    }
});