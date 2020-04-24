$(document).ready(function() {
    $('.get_share_link').click(function() {
        var user_id = $(this).attr('user_id')
        var data = {'user_id': user_id}
        console.log(user_id)

        req = $.ajax({
            url : 'get_temporary_vip1/get_share_code',
            type : 'POST',
            data: JSON.stringify(data),
            contentType: 'application/json; charset=UTF-8',
            success: function(data){},
            error: function(xhr, type) {}
        });

        req.done(function(data) {
            $('#share_link').html(data);
        });
        console.log(data)
    });
});