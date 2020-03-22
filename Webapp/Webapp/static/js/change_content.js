$(document).ready(function() {
    $('#buysbutton').click(function() {
        var category = 'like';

        req = $.ajax({
            url : 'user/account/update',
            type : 'POST',
            data : {category : category}
        });

        req.done(function(data) {
            $('#content').fadeOut(1000).fadeIn(1000);
            $('#content').text(data.deals);
        });
    });


});