;
var user_edit_ops = {
    init:function(){
        this.eventBind();
    },
    eventBind:function(){
        $(".user_edit_wrap .save").click( function(){
               var btn_target = $(this);
               if (btn_target.hasClass("disabled")){
                    common.ops.alert("Processing...")
                    return;
               }

               var nickname_target = $(".user_edit_wrap input[name=nickname]");
               var nickname = nickname_target.val();

               var email_target = $(".user_edit_wrap input[name=email]");
               var email = email_target.val();

               if(!nickname || nickname.length < 2){
                    common_ops.tip("Please input name in good format", nickname_target)
                    return false;
               }
               if(!email || email.length < 2){
                    common_ops.tip("Please input email in good format", email_target)
                    return false;
               }

               btn_target.addClass("disabled");
               var data = {
                    nickname:nickname,
                    email:email
               }
               $.ajax({
                   url:common_ops.buildUrl("/user/edit"),
                   type:'POST',
                   data:data,
                   dataType:'json',
                   success:function(res){
                     var callback = null;
                     if(res.code == 200){
                        btn_target.removeClass('disabled');
                        callback = function(){
                            // refresh current page
                            window.location.href = window.location.href;
                        }
                        common_ops.alert(res.msg, callback)
                     }
                   }
               });

        });
    }
};

$(document).ready(function(){
    user_edit_ops.init();
});