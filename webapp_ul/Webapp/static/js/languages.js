$(document).ready(function(){
    var tnum = $('.current_lang').attr('default')
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
    $('.current_lang').attr('default', lang);

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
    $('.forget-password-text').text(trans[28][tnum])
//register
    $('#register-title').text(trans[29][tnum])
    $('.username-text').text(trans[30][tnum])
    $('.confirm-password-text').text(trans[31][tnum])
    $('#register-bottom-text').text(trans[32][tnum])
    $('#register-sign-in').text(trans[33][tnum])
//account
    $('#update-profile-text').text(trans[34][tnum])
    $('#change-profile-pic-text').text(trans[35][tnum])
    $('#change-password-text').text(trans[36][tnum])
    $('#invitation-text').text(trans[37][tnum])
    $('#likes').text(trans[38][tnum])
    $('#similar').text(trans[39][tnum])
//edit profile
    $('.new-email-text').text(trans[40][tnum])
    $('.confirm-new-email-text').text(trans[41][tnum])
//edit avater
    $('.avater-text').text(trans[42][tnum])
//change password
    $('.old-password').text(trans[43][tnum])
        $('.new-password').text(trans[44][tnum])
            $('.confirm-new-password').text(trans[45][tnum])
            //request reset
    $('#request-reset-title').text(trans[46][tnum])
                //reset token
    $('#reset-password-title').text(trans[47][tnum])
    // account vip
    // code submit
        $('#code-submit-title').text(trans[48][tnum])
            $('.code-text').text(trans[49][tnum])
    // temporary vip
     $('#temporary-vip1-button').text(trans[50][tnum])
            $('#temporary-vip2-button').text(trans[51][tnum])
    // vip code
        $('#vip-text1').text(trans[52][tnum])
        $('#vip-text2').text(trans[53][tnum])
        $('#vip1-code-text').text(trans[54][tnum])
        $('#vip2-code-text').text(trans[55][tnum])
        $('#buy-vip-link').text(trans[56][tnum])
        $('.buy-vip-button').text(trans[57][tnum])



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
    },{
    en:'Join today',
    cn:'注册'
    },{
    en:'User name',
    cn:'用户名'
    },{
    en:'Confirm password',
    cn:'确认密码'
    },{
    en:'Already have an account?',
    cn:'已经拥有账户?'
    },{
    en:'Sign in',
    cn:'登录'
    },{
    en:'Edit Profile',
    cn:'编辑账户'
    },{
    en:'Change Avater',
    cn:'更改头像'
    },{
    en:'Change Password',
    cn:'更改密码'
    },{
    en:'Invitation code',
    cn:'填写邀请码'
    },{
    en:'Your favourite',
    cn:'你的收藏'
    },{
    en:'You may like',
    cn:'你可能喜欢的'
    },{
    en:'New Email',
    cn:'新邮箱'
    },{
    en:'Confirm New Email',
    cn:'确认新邮箱'
    },{
    en:'Upload new avater',
    cn:'上传新头像'
    },{
    en:'Old Password',
    cn:'旧密码'
    },{
    en:'New Password',
    cn:'新密码'
    },{
    en:'Confirm New Password',
    cn:'确认新密码'
    },{
    en:'Request Reset',
    cn:'请求重置'
    },{
    en:'Reset Password',
    cn:'重置密码'
    },{
    en:'Submit invitation code',
    cn:'提交邀请码'
    },{
    en:'Invitation code',
    cn:'提交邀请码'
    },{
    en:'Get your VIP1 for 3 days',
    cn:'获得三天免费VIP1体验'
    },{
    en:'Get your VIP2 for 1 day',
    cn:'获得一天免费VIP2体验'
    },{
    en:'You already used your free vip service, do you like our content?',
    cn:'您已经使用过你的免费vip服务了, 您喜欢我们的内容吗?'
    },{
    en:'Use your invitation code, let a new submit your invitation code to get additional free vip service.',
    cn:'让一个新用户提交你的邀请码, 您将可以获得额外的免费VIP体验哦。'
    },{
    en:'Your invitation code for VIP1:',
    cn:'您的VIP1邀请码: '
    },{
    en:'Your invitation code for VIP2',
    cn:'您的VIP2 邀请码: '
    },{
    en:'Or buy new VIP service.',
    cn:'或者您可以购买新的VIP服务。'
    },{
    en:'Buy your VIP',
    cn:'购买VIP'
    }

];