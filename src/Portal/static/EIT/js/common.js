jQuery(function($){

    var arrWidthNot = [];
    $(".circle-csutom-notif").each(function() {
        var w = $(this).find("span").width();
        arrWidthNot.push(parseInt(w)+7);
    });


    var maxWidth = Math.max.apply(null,arrWidthNot)

    $(".circle-csutom-notif").each(function(){

        if($(this).attr("syncsize") == "1") {
            $(this).css("width", maxWidth.toString() + "px");
            $(this).css("height", maxWidth.toString() + "px");
            var background = $(this).attr("background");
            var color = $(this).attr("color");
            var size = $(this).attr("size");
            var font = $(this).attr("font");
            if (background != "") {
                $(this).css("background-color", background);
            }
            if (color != "") {
                $(this).find("span").css("color", color);
            }
            if (size != "") {
                $(this).find("span").css("font-size", size + "px");
            }
            if (font != "") {
                $(this).find("span").css("font-family", font);
            }
        }
        });


    /*$("*[class*='js_style_']").each(function(){
        var arr = $(this).attr("class").split(" ");
        var elm = $(this);
        arr.forEach(function(item){
            if(item.indexOf("js_style_") > -1){
                var style = item.split("_")[2];
                var val = item.split("_")[3];
                elm.css(style,val);
            }
        });

    });*/


    $(".js_style").each(function(){
        var arr = $(this).attr("class").split(" ");
        var elm = $(this);
        arr.forEach(function(item){
            if(item.indexOf("js_style_") > -1){
                var style = item.split("_")[2];
                var val = item.split("_")[3];
                val = val.replaceAll("$$",' ');
                elm.css(style,val);
            }
        });

    });


    //custom data table bootstrap 5
    setTimeout(function(){
        var clondLeabel = $(".dataTables_filter").find("label").clone(true);
        $(".dataTables_filter").find("label").remove();
        $(".dataTables_filter").append('<span style="margin-left:5px;">فیلتر : </span>');
        $(".dataTables_filter").append(clondLeabel.children()[0]);
        $(".dataTables_filter").css({
            display:'flex',
            flexDirection:'row',
            justifyContent:'end',
            alignItems:'center',
        });


        var clondLeabel = $(".dataTables_length").find("label").clone(true);
        $(".dataTables_length").find("label").remove();
        $(".dataTables_length").append('<span style="margin-left:5px;"> نمایش </span>');
        $(".dataTables_length").append(clondLeabel.children()[0]);
        $(".dataTables_length").append('<span style="margin-right:5px;"> سطر </span>');
        $(".dataTables_length").css({
            display:'flex',
            flexDirection:'row',
            justifyContent:'start',
            alignItems:'center',
        });
        $(".dataTables_length").find("select").on("change",function(){
            $(".dataTables_paginate.paging_simple_numbers").find("ul").find("li.page-item.previous").find("a").html("قبلی");
            $(".dataTables_paginate.paging_simple_numbers").find("ul").find("li.page-item.next").find("a").html("بعدی");
        });

        $(".dataTables_info").hide();

        $(".dataTables_paginate.paging_simple_numbers").find("ul").find("li.page-item.previous").find("a").html("قبلی");
        $(".dataTables_paginate.paging_simple_numbers").find("ul").find("li.page-item.next").find("a").html("بعدی");
        $(".dataTables_paginate.paging_simple_numbers").css({
            display:'flex',
            flexDirection:'row',
            justifyContent:'end',
            alignItems:'center',
        });

        $(".dataTables_empty").html('');

        $(".dataTables_filter .form-control").on('input',function(){
            $(".dataTables_paginate.paging_simple_numbers").find("ul").find("li.page-item.previous").find("a").html("قبلی");
            $(".dataTables_paginate.paging_simple_numbers").find("ul").find("li.page-item.next").find("a").html("بعدی");
            $(".dataTables_empty").html('');
        });

        $(document).delegate("a.page-link",'click',function(){
            $(".dataTables_paginate.paging_simple_numbers").find("ul").find("li.page-item.previous").find("a").html("قبلی");
            $(".dataTables_paginate.paging_simple_numbers").find("ul").find("li.page-item.next").find("a").html("بعدی");
            $(".dataTables_empty").html('');
        });
    },200);


    //.fix-input-to-line
    $(".fix-input-to-outline").each(function(){
        var elm = $(this);
        if(elm.val().length > 0) {
            elm.addClass("active");
        }
    });
    


});