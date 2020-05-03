var tnum = 'en';

$(document).ready(function(){
  $(document).click( function(e) {
       $('.translate_wrapper, .more_lang').removeClass('active');
  });

  $('.translate_wrapper .current_lang').click(function(e){    
    e.stopPropagation();
    $(this).parent().toggleClass('active');
    
    setTimeout(function(){
      $('.more_lang').toggleClass('active');
    }, 5);
  });
  

  /*TRANSLATE*/
  translate(tnum);
  
  $('.more_lang .lang').click(function(){
    $(this).addClass('selected').siblings().removeClass('selected');
    $('.more_lang').removeClass('active');  
    
    var img = $(this).find('img').attr('src');    
    var lang = $(this).attr('data-value');
    var tnum = lang;
    translate(tnum);
    
    $('.current_lang .lang-txt').text(lang);
    $('.current_lang img').attr('src', img);
    
    if(lang == 'ar'){
      $('body').attr('dir', 'rtl');
    }else{
      $('body').attr('dir', 'ltr');
    }
    
  });
});

function translate(tnum){
  $('#app_name').text(trans[0][tnum]);
  $('#account_button').text(trans[1][tnum]);
  $('#logout_button').text(trans[2][tnum]);
  $('#login_button').text(trans[3][tnum]);
  $('#register_button').text(trans[4][tnum]);
  $('#ToTopButton').text(trans[5][tnum]);
  $('#search_welcome').text(trans[6][tnum])

}

var trans = [ 
  { 
    en : 'My Muses',
    cn : '女神网',
  },{
      en : 'Account',
      cn : '账户',
  },{
    en : 'Log out',
    cn : '登出',
  },{
      en : 'Log in',
      cn : '登录',
    },{
    en : 'Register',
    cn : '注册',
    },{
    en: 'Back to top',
    cn: '返回顶部'
    },{
    en: 'Back to top',
    cn: '返回顶部'
    },{
    en: 'Type to search',
    cn: '搜索'
    }


];