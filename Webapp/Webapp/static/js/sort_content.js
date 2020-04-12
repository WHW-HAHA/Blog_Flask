$(document).ready(function() {
    $('.dropdown-item').click(function() {
        var by = $(this).attr('name');
        console.log(by)
        var categoryName = $(this).attr('category')
        console.log(categoryName)
        if (categoryName == 'The latest'){
            categoryName = 'TheLatest'}
        if (categoryName == 'Europe & USA'){
            categoryName = 'Europe&USA'}
        var data = {'by': by,
                    'categoryName': categoryName}

        console.log(data)
        req = $.ajax({
            url : categoryName + '/sorted',
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