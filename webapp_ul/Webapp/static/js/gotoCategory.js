$(document).ready(function() {
    $('.gotoContentButton').click(function() {
        var category = $(this).attr('id');
        var data = {'category': category}
        console.log(data)
        req = $.ajax({
            url : '/gotocategory',
            type : 'POST',
            data: JSON.stringify(data),
            contentType: 'application/json; charset=UTF-8',
            success: function(data){},
            error: function(xhr, type) {}
        });

        console.log('Function Done')

//        req.done(function(data) {
//            $('#content').fadeOut(100).fadeIn(100);
//            $('#content').html(data);
        console.log('Function2 Done')

        });
    });
//});