//
// django.jQuery(function($){
//     $(".selector").remove();
//     $(".module.aligned").append('<div class="new-data"></div>');
//     $(".new-data").load('/InternalAccess/GetPermissionsAsHtml/');
//
//     if($("#id_Apps")!=undefined){
//         $("#id_Apps").select2();
//         if($("#id_Apps").attr("data-form") == "PermissionUserForm"){
//
//             $("#id_User").select2();
//             var url = $("#id_Apps").attr("ajaxurl");
//             $("#id_User").on('change',function(){
//                 var app = $("#id_Apps").val();
//                 var user = $("#id_User").val();
//                 get_user_permission(app,user,"id_Permissions",url);
//             });
//
//             $("#id_Apps").on('change',function(){
//                 var app = $("#id_Apps").val();
//                 var user = $("#id_User").val();
//                 get_user_permission(app,user,"id_Permissions",url);
//             });
//
//
//             init_permissions();
//
//         }
//
//         else if($("#id_Apps").attr("data-form") == "GroupPermissionForm"){
//
//             var parent_id_oldgroup = $("#id_Old_group").parent();
//             $("#id_Old_group").remove();
//             parent_id_oldgroup.append(`<select name="Old_group" id="id_Old_group"></select>`)
//             $("#id_Old_group").select2();
//             $("#id_Old_group").css("width","60%");
//             $("#id_Old_group").next().css("width","60%");
//             $("#id_Apps").on('change',function(){
//                 get_group_names($(this).val(),"id_Old_group",$("#id_Apps").attr("ajaxurlgetgroup"));
//             });
//             $("#id_New_group").on('input',function(){
//                 if($(this).val().length > 0){
//                     $("#id_Old_group").parent().hide();
//                     $("#id_Permissions").parent().hide();
//                 }
//                 else{
//                     $("#id_Old_group").parent().show();
//                     $("#id_Permissions").parent().show();
//                 }
//             });
//
//             $(document).delegate("#id_Old_group",'change',function(){
//                 var app = $("#id_Apps").val();
//                 var group = $("#id_Old_group").val();
//                 var url = $("#id_Apps").attr("ajaxurlgetgrouppermissions");
//                 get_group_permissions(app,group,"id_Permissions",url);
//             });
//
//             init_permissions();
//
//
//         }
//
//         else if($("#id_Apps").attr("data-form") == "UserGroupForm"){
//             var parent_id_group = $("#id_Group").parent();
//             $("#id_Group").remove();
//             parent_id_group.append(`<select name="Group" id="id_Group"></select>`)
//             $("#id_Group").select2();
//             $("#id_Group").css("width","60%");
//             $("#id_Group").next().css("width","60%");
//             $("#id_User").select2();
//             $("#id_User").css("width","60%");
//             $("#id_User").next().css("width","60%");
//             $("#id_Apps").on('change',function(){
//                 get_group_names($(this).val(),"id_Group",$("#id_Apps").attr("ajaxurlgetgroup"));
//             });
//
//             $(document).delegate('#id_Group','change',function(){
//                 var app = $("#id_Apps").val();
//                 var group = $("#id_Group").val();
//                 get_users_in_group(app,group,"id_User",$("#id_Apps").attr("ajaxurlgetysersgroup"));
//             });
//         }
//     }
//
//
//
//
//
//
//     function get_users_in_group(app,group,id,url){
//         var id_from = id+"_from";
//         var id_to = id+"_to";
//         $.ajax({
//             'url': url,
//             'type': 'POST',
//             'data': {
//                 'app': app,
//                 'group':group,
//                 'csrfmiddlewaretoken': document.getElementsByName('csrfmiddlewaretoken')[0].value
//             },
//             'success': function (res) {
//                 if(res.state == "ok"){
//                     $("#"+id_to+" option").remove();
//                     $("#"+id_from+" option").each(function(){
//                         if(res.data.rows.indexOf($(this).val()) > -1 ){
//                             $("#"+id_to).append($(this).clone())
//                             $(this).remove();
//                         }
//                     });
//                 }
//             }
//         });
//     }
//
//     function get_group_permissions(app,group,id,url){
//         var id_from = id+"_from";
//         var id_to = id+"_to";
//         $.ajax({
//             'url': url,
//             'type': 'POST',
//             'data': {
//                 'app': app,
//                 'group':group,
//                 'csrfmiddlewaretoken': document.getElementsByName('csrfmiddlewaretoken')[0].value
//             },
//             'success': function (res) {
//                 if(res.state == "ok"){
//
//                     $("#"+id_from).empty();
//                     $("#"+id_to).empty();
//                     var ops = '';
//                     res.data.rows_all.forEach(function(item){
//                         ops+=`<option value="${item.id}">${item.text}</option>`;
//                     });
//                     $("#"+id_from).append(ops);
//                     var selected_ops = '';
//                     res.data.rows_group.forEach(function(item){
//                         selected_ops+=`<option value="${item.id}">${item.text}</option>`;
//                     });
//                     $("#"+id_to).append(selected_ops);
//
//                 }
//             }
//         });
//     }
//
//
//     function get_group_names(app,id,url){
//         $.ajax({
//             'url': url,
//             'type': 'POST',
//             'data': {
//                 'app': app,
//                 'csrfmiddlewaretoken': document.getElementsByName('csrfmiddlewaretoken')[0].value
//             },
//             'success': function (res) {
//                 if(res.state == "ok"){
//
//                         var par = $("#"+id).parent();
//                         par.children().each(function(){
//                             if($(this).prop('tagName') != "LABEL"){
//                                 $(this).remove();
//                             }
//                         });
//                         par.append(`<select name="${id.replace('id_','')}" id="${id}"></select>`)
//                         $("#"+id).select2({
//                             'data':res.data.rows,
//                         });
//                         $("#"+id).css("width","60%");
//                         $("#"+id).next().css("width","60%");
//
//                         $("#"+id).select2().val(res.data.rows[0].id).trigger('change')
//
//                 }
//             }
//         });
//     }
//
//     function get_user_permission(app,user,id,url){
//         var id_from = id+"_from";
//         var id_to = id+"_to";
//         $.ajax({
//             'url':url,
//             'type':'POST',
//             'data':{'app':app,'user':user,'csrfmiddlewaretoken': document.getElementsByName('csrfmiddlewaretoken')[0].value},
//             'success':function(res) {
//                 if (res.state == "ok") {
//                     var data = [];
//                     var vals = []
//                     var arr = res.data.perms;
//                     var arr_selected = res.data.selected_perms;
//                     var ops = '';
//                     var selected_ops = '';
//                     arr.forEach(function(item){
//                         data.push({'id':item[2],'text':item[0]+' | '+item[4]})
//                         ops+=`<option value="${item[2]}">${item[0]+' | '+item[4]}</option>`;
//                     });
//                     arr_selected.forEach(function(item){
//                         vals.push(item[2])
//                         selected_ops+=`<option value="${item[2]}">${item[0]+' | '+item[4]}</option>`;
//                     });
//                     $("#"+id_from).empty();
//                     $("#"+id_from).append(ops);
//                     $("#"+id_to).empty();
//                     $("#"+id_to).append(selected_ops);
//                     /*if(data.length > 0){
//                         if($("#"+id+" option").length>1) {
//                             $("#"+id).children().each(function(){
//                                 if($(this).prop('tagName') != "SELECT" && $(this).prop('tagName') != "LABEL"){
//                                     $(this).remove();
//                                 }
//                             });
//                         }
//                         $("#"+id).select2({
//                             data:data,
//                             multiple:true,
//                         });
//                         $("#"+id).select2().val(vals).trigger("change")
//                     }*/
//                 }
//             }
//         });
//     }
//
//     function init_permissions(){
//             setTimeout(function(){
//                 var elm_id_Permissions_add_all_link = $("#id_Permissions_add_all_link").clone();
//                 elm_id_Permissions_add_all_link.attr("id","id_Permissions_add_all_link_new");
//                 elm_id_Permissions_add_all_link.removeAttr("href");
//                 elm_id_Permissions_add_all_link.attr("style","cursor:pointer;");
//                 $("#id_Permissions_add_all_link").after(elm_id_Permissions_add_all_link);
//                 $("#id_Permissions_add_all_link").remove();
//
//                 var elm_id_Permissions_remove_all_link = $("#id_Permissions_remove_all_link").clone();
//                 elm_id_Permissions_remove_all_link.attr("id","id_Permissions_remove_all_link_new");
//                 elm_id_Permissions_remove_all_link.attr("style","cursor:pointer;");
//                 elm_id_Permissions_remove_all_link.removeAttr("href");
//                 $("#id_Permissions_remove_all_link").after(elm_id_Permissions_remove_all_link);
//                 $("#id_Permissions_remove_all_link").remove();
//
//                 var elm_selector_chooser = $(".selector-chooser").clone();
//                 elm_selector_chooser.attr("id","selector_chooser_new");
//                 elm_selector_chooser.find("a").each(function(){
//                     $(this).attr("id","id_Permissions_add_link_new");
//                     $(this).removeAttr("href");
//                     $(this).attr("style","cursor:pointer;");
//                 });
//                 $(".selector-chooser").after(elm_selector_chooser);
//                 $(".selector-chooser").not("#selector_chooser_new").remove();
//
//             },500);
//
//             $("#id_Permissions_from").empty();
//
//             $(document).delegate("#id_Permissions_add_all_link_new",'click',function(){
//                 var vals = [];
//                 $("#id_Permissions_from option").each(function(){
//                     vals.push($(this).attr("value"))
//                 });
//                 $("#id_Permissions_from").val(vals).trigger("change");
//             });
//
//             $(document).delegate(".selector-add",'click',function(){
//                 var arr = $("#id_Permissions_from").val();
//                 $("#id_Permissions_from option").each(function(){
//                     if(arr.indexOf($(this).attr("value")) >-1 ){
//                         $("#id_Permissions_to").append($(this)[0]);
//                         //$(this).remove();
//                     }
//                 });
//             })
//
//             $(document).delegate(".selector-remove",'click',function(){
//                 var arr_from = [];
//                 var tmp = $("#id_Permissions_from").children();
//                 for(var i = 0; i< tmp.length;i++){
//                     var item = tmp[i];
//                     arr_from.push(item.getAttribute("value"));
//                 }
//
//                 var arr = $("#id_Permissions_to").val();
//                 $("#id_Permissions_to option").each(function(){
//                     if(arr.indexOf($(this).attr("value")) >-1 && arr_from.indexOf($(this).attr("value")) == -1 ){
//                         $("#id_Permissions_from").append($(this)[0]);
//                     }
//                     if(arr.indexOf($(this).attr("value")) >-1){
//                         $(this).remove();
//                     }
//                 });
//             });
//
//             $(document).delegate("#id_Permissions_remove_all_link_new","click",function(){
//                 var arr = [];
//                 var tmp = $("#id_Permissions_from").children();
//                 for(var i = 0; i< tmp.length;i++){
//                     var item = tmp[i];
//                     arr.push(item.getAttribute("value"));
//                 }
//                 $("#id_Permissions_to option").each(function(){
//                     if(arr.indexOf($(this).attr("value")) == -1)
//                         $("#id_Permissions_from").append($(this)[0]);
//                 });
//                 $("#id_Permissions_to").empty();
//             });
//     }
//
// });