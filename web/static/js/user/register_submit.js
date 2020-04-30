;
// Through js enhance user experience. Do not need to send to backend to make a judgement every time
var user_register_submit_ops=  {
    init:function(){
        this.eventBind();
    },
    eventBind:function(){
        $(".login_wrap .do-submit").click( function(){
            var btn_target = $(this)
            if(btn_target.hasClass('disabled')){
                common_ops.alert("Processing..")
                return;
            }
            var user_name = $(".login_wrap input[name=user_name]").val();
            var password = $(".login_wrap input[name=password]").val();
            var phone_number = $(".login_wrap input[name=phone_number]").val();
            var email = $(".login_wrap input[name=email]").val();
            var first_name = $(".login_wrap input[name=first_name]").val();
            var middle_name = $(".login_wrap input[name=middle_name]").val();
            var last_name = $(".login_wrap input[name=last_name]").val();
            var occupation = $(".login_wrap input[name=occupation]").val();
            var mail_address = $(".login_wrap input[name=mail_address]").val();

            if(user_name == undefined || user_name.length<1){
                common_ops.alert("Username is empty!");
                return;
            }
            if(password == undefined || password.length<1){
                common_ops.alert("Password is empty!");
                return;
            }
            if(phone_number == undefined || phone_number.length<1){
                common_ops.alert("phone number is empty!");
                return;
            }
            if(email == undefined || email.length<1){
                common_ops.alert("email is empty!");
                return;
            }
            if(first_name == undefined || first_name.length<1){
                common_ops.alert("first name is empty!");
                return;
            }
            if(last_name == undefined || last_name.length<1){
                common_ops.alert("last name is empty!");
                return;
            }

            $.ajax({
                url:common_ops.buildUrl("/user/register_submit"),
                type:'POST',
                data:{ 'user_name':user_name,'password':password,'phone_number':phone_number,'email':email,'first_name':first_name,'middle_name':middle_name,'last_name':last_name,'occupation':occupation,'mail_address':mail_address },
                dataType:'json',
                // res get from backend
                success:function(res){
                // leave out side if
                     btn_target.removeClass('disabled');
                     if(res.code == 200){
                        alert("Success!");
                        window.location.href = common_ops.buildUrl("/");
                     }
                     if(res.code == -1){
                        alert("Username already exists, please input a new username!");
                        $(".login_wrap input[name=user_name]").val('');
                     }
                     // no matter login right or wrong response with the alert
                }
            });
        });
    }
};

$(document).ready( function(){
    user_register_submit_ops.init();
});