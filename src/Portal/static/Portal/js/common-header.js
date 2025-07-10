
    jQuery(document).ready(function($){
        $("#fake_user_combo").select2();
        $("#fake_user_combo").on('select2:select',function(e){
            $(".div-loader-base").show()
            var data = e.params.data;
            var csrf = $("[name='csrfmiddlewaretoken']").val();
            var next_url = location.protocol + '//' + location.host + location.pathname;
            $.post(`/Portal/GenerateLinkFakeUser/`,{'change_to_username':data.id,'csrfmiddlewaretoken':csrf,'next_url':next_url},function(data){
                if(data.state == "ok"){
                    window.location.href = data.url;
                } else if (data.state == "error"){
                    alert(data.details); 
                    window.location.href = "/?delegate_logout=1";
                }
            })
        });

        $("#exit_current_login").on('click',function(){
            $(".div-loader-base").show()
            window.location.href = "/?delegate_logout=1";
        });

        setTimeout(checkImageNotExists,500);
        function checkImageNotExists(){
            var img = document.querySelector(".img-profile");
            var src = img.getAttribute("default-src");//(img.getAttribute("gender") == "m") ? img.getAttribute("default-src-m") : img.getAttribute("default-src-f");
            if(img.naturalWidth ==0 ) {
                img.setAttribute("src", src);
            }
        }

    })