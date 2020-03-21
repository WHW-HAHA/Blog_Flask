$(document).ready(function() {

    $('#buysbutton').on('click', function() {
        var category = 'like';
        console.log(category)

        req = $.ajax({
            url : '/update',
            type : 'POST',
            data : {category : category}
        });

        req.done(function(data) {
            $('#content').fadeOut(1000).fadeIn(1000);
            $('#content').text(data.deals);
        });
    });


});