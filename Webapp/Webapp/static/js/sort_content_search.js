$(document).ready(function() {
    $('.dropdown-item').click(function() {
        var by = $(this).attr('name');
        var keyword = $(this).attr('keyword');
        var data = {'by': by,
                    'keyword': keyword}

        console.log(data)
        req = $.ajax({
            url : 'search' + '/sorted',
            type : 'POST',
            data: JSON.stringify(data),
            contentType: 'application/json; charset=UTF-8',
            success: function(data){},
            error: function(xhr, type) {}
        });

        console.log('Function1 Done')

        req.done(function(data) {
            $('#content').fadeOut(100).fadeIn(100);
            $('#content').html(data);
        console.log('Function2 Done')

        });
    });
});