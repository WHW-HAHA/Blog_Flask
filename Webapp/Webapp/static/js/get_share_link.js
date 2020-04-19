$(document).ready(function() {
    $('.get_share_link').click(function() {
        var user_id = $(this).attr('user_id')
        console.log(user_id)

        req = $.ajax({
            url : '/get_share_code',
            type : 'POST',
            data: JSON.stringify(data),
            contentType: 'application/json; charset=UTF-8',
            success: function(data){},
            error: function(xhr, type) {}
        });

        console.log('share_link' + post_id)

        });
    });
});