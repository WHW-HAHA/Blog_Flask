$(document).ready(function() {
    $('.category').click(function() {
        var category = $(this).attr('id');
        var data = {'category': category}
        var language = localStorage.getItem('locale') || window.navigator.language.toLowerCase() || 'en'
        if (language.indexOf("zh-") !== -1) {
        var tnum = 'cn'
        } else if (language.indexOf('en') !== -1) {
            var tnum = 'en'
        } else {
            var tnum = 'en'
        }

        console.log(data)
        if (tnum == 'en'){
        req = $.ajax({
            url : 'en/account/update',
            type : 'POST',
            data: JSON.stringify(data),
            contentType: 'application/json; charset=UTF-8',
            success: function(data){},
            error: function(xhr, type) {}
        });} else if (tnum == 'cn'){
        req = $.ajax({
            url : 'cn/account/update',
            type : 'POST',
            data: JSON.stringify(data),
            contentType: 'application/json; charset=UTF-8',
            success: function(data){},
            error: function(xhr, type) {}
        });}


        console.log('Function1 Done')

        req.done(function(data) {
            $('#content').fadeOut(100).fadeIn(100);
            $('#content').html(data);
        console.log('Function2 Done')

        });
    });
});