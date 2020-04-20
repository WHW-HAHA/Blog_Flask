$(document).ready(function() {
    $(document).on('click', '.aheart', function() {
        var post_title = $(this).attr('post_title')
        var post_id = $(this).attr('post_id')
        var prime_post_id = $('prime_post').attr('post_id')
        var data = {'post_title': post_title,
                    'prime_post_id': prime_post_id}
        console.log(data)

        req = $.ajax({
            url : + prime_post_id +'/add_favourite',
            type : 'POST',
            data: JSON.stringify(data),
            contentType: 'application/json; charset=UTF-8',
            success: function(data){},
            error: function(xhr, type) {}
        });

        req.done(function(data) {
            $('#post_content_section' + post_id).fadeOut(100).fadeIn(100);
            $('#post_content_section' + post_id).html(data);
        });
    });
});