;
var mod_pwd_ops = {
    init:function(){
        this.eventBind();
    },
    eventBind:function(){
        $(".do-modify").click(function(){
            var btn_target = $(this);
            if( btn_target.hasClass("disabled") ){
                common_ops.alert("Processing..");
                return;
            }

            var old_password = $("input[name=old_password]").val();
            var new_password = $("input[name=new_password]").val();
            var new_password2 = $("input[name=new_password2]").val();

            if (new_password!=new_password2){
                common_ops.alert( "Confirmation not match!" );
                $("input[name=new_password2]").val('');
                $("input[name=new_password2]").append('<style>.confirmation::placeholder{color:red; opacity:0.4;}</style>');
                return false
            }

            if( !old_password ){
                common_ops.alert( "Please Input Old Password!" );
                return false;
            }

            if( !new_password || new_password.length < 1 ){
                common_ops.alert( "Please Input New Password!" );
                return false;
            }

            if (old_password == new_password){
                common_ops.alert("Same New Password and Old Password!")
                $("input[name=new_password]").val('');
                $("input[name=new_password]").append('<style>.new_password::placeholder{color:red; opacity:0.4;}</style>');
                $("input[name=new_password2]").val('');
                $("input[name=new_password2]").append('<style>.confirmation::placeholder{color:red; opacity:0.4;}</style>');
                return false;
            }


            btn_target.addClass("disabled");

            var data = {
                old_password: old_password,
                new_password: new_password
            };

            $.ajax({
                url:common_ops.buildUrl( "/user/reset-pwd" ),
                type:'POST',
                data:data,
                dataType:'json',
                success:function( res ){
                    btn_target.removeClass("disabled");
                    var callback = null;
                    if( res.code == 200 ){
                        callback = function(){
                            window.location.href = common_ops.buildUrl("/");
                        }
                    }
                    common_ops.alert( res.msg,callback );
                }
            });


        });
    }
};

$(document).ready( function(){
    mod_pwd_ops.init();
} );