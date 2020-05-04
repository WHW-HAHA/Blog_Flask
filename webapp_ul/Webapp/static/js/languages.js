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
// welcome section
  $('#app_name').text(trans[0][tnum]);
  $('#account_button').text(trans[1][tnum]);
  $('#logout_button').text(trans[2][tnum]);
  $('#login_button').text(trans[3][tnum]);
  $('#register_button').text(trans[4][tnum]);
  $('#ToTopButton').text(trans[5][tnum]);
  $('.asia_category_name').text(trans[6][tnum])
  $('.asia_category_description').text(trans[7][tnum])
  $('.usa_category_name').text(trans[8][tnum])
  $('.usa_category_description').text(trans[9][tnum])
  $('.cartoon_category_name').text(trans[10][tnum])
  $('.cartoon_category_description').text(trans[11][tnum])
  $('.see-more').text(trans[12][tnum])
  $('.latest_button').text(trans[13][tnum])
//  category section
  $('#btnGroupDrop1').text(trans[14][tnum])
  $('.sort-1').text(trans[15][tnum])
  $('.sort-2').text(trans[16][tnum])
  $('.vip1-text').text(trans[17][tnum])
  $('.vip2-text').text(trans[18][tnum])
//  search section
    $('#header_search_found').text(trans[19][tnum])
    $('#header_search_not_found').text(trans[20][tnum])
    $('.back-to-home').text(trans[21][tnum])
//log in
    $('#login_title').text(trans[22][tnum])
    $('.email-text').text(trans[23][tnum])
    $('.password-text').text(trans[24][tnum])
    $('.remember-me').text(trans[25][tnum])
    $('.submitbutton').text(trans[26][tnum])
    $('.forget-password-text').text(trans[27][tnum])
//register
    $('#login_title').text(trans[22][tnum])
    $('.email-text').text(trans[23][tnum])
    $('.password-text').text(trans[24][tnum])
    $('.remember-me').text(trans[25][tnum])
    $('.submitbutton').text(trans[26][tnum])
    $('.forget-password-text').text(trans[27][tnum])

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
    en: 'Asia',
    cn: '亚洲'
    },{
    en: 'Soft as water',
    cn: '柔情似水'
    },{
    en: 'Europe & USA',
    cn: '欧美'
    },{
    en: 'Like fire',
    cn: '热情似火'
    },{
    en: 'Cartoon',
    cn: '二次元'
    },{
    en: 'Perfect virtual lover',
    cn: '虚拟世界中的完美情人'
    },{
    en: 'Explore more',
    cn: '查看更多'
    },{
    en: 'The latest',
    cn: '最新发布'
    },{
    en: 'Sort',
    cn: '排序'
    },{
    en: 'By popularity',
    cn: '按照受欢迎程度'
    },{
    en: 'By date',
    cn: '按照发布时间'
    },{
    en: 'Only available for VIP1',
    cn: '只对VIP1用户开放'
    },{
    en: 'Only available for VIP2',
    cn: '只对VIP2用户开放'
    },{
    en:'We have found these interesting contents for you.',
    cn:'我们为您找到这些相关的内容.'
    },{
    en:'Sorry, no content has been found.',
    cn:'抱歉，我们没能找到任何内容'
    },{
    en:'Back to home page',
    cn:'回到主页'
    },{
    en:'Please login',
    cn:'请登录'
    },{
    en:'Email',
    cn:'邮箱'
    },{
    en:'Password',
    cn:'密码'
    },{
    en:'Remember me',
    cn:'保持我的登录'
    },{
    en:'Remember me',
    cn:'保持我的登录'
    },{
    en:'Submit',
    cn:'提交'
    },{
    en:'Forget password?',
    cn:'忘记密码?'
    }

];