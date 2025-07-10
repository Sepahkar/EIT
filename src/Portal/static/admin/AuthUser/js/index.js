django.jQuery(function($){
    $("#id_to_user").select2();
    $("#id_to_user").css("max-width","30%");
    $("#id_to_user").next().css("max-width","30%");

    $("[name='_addanother']").hide();
    $("[name='_continue']").hide();
    $("[name='_save']").attr("value","جابجایی");
    $("[name='_save']").css("font-size","17px");
    $("[name='_save']").css("font-weight","bold");

});