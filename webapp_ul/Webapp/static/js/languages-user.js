$(document).ready(function(){
    var language = localStorage.getItem('locale') || window.navigator.language.toLowerCase() || 'en'
    localStorage.setItem('locale', language)
//    getdefaultlang()
    if (language.indexOf("zh-") !== -1) {
        var lang = 'cn'
    } else if (language.indexOf('en') !== -1) {
        var lang = 'en'
    } else {
        var lang = 'en'
    }

    var data = {'lang': lang}
    console.log(data)
    req = $.ajax({
        url : 'user/login/language',
        type : 'POST',
        data: JSON.stringify(data),
        contentType: 'application/json; charset=UTF-8',
        success: function(data){},
        error: function(xhr, type) {}
    });
}


