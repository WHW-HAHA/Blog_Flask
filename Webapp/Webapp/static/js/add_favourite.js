$(document).ready(function() {
    $('.add_favourite').click(function() {
        var post_title = $(this).attr('post_title')
        var categoryName = $(this).attr('category')
        var post_id = $(this).attr('post_id')
        if (categoryName == 'The latest'){
            categoryName = 'TheLatest'}
        if (categoryName == 'Europe & USA'){
            categoryName = 'Europe&USA'}
        var data = {'post_title': post_title,
                    'categoryName': categoryName,
                    }
        console.log(data)

        console.log(data)
        req = $.ajax({
            url : + categoryName + '/add_favourite',
            type : 'POST',
            data: JSON.stringify(data),
            contentType: 'application/json; charset=UTF-8',
            success: function(data){},
            error: function(xhr, type) {}
        });

        console.log('post_content_section' + post_id)

        req.done(function(data) {
            $('#post_content_section' + post_id).fadeOut(100).fadeIn(100);
            $('#post_content_section' + post_id).html(data);

        });
    });
});