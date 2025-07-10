/**********************************General Function*******************/
function HasAttr(item, attr)
{
    a = $(item).attr(attr);
    return typeof attr !== 'undefined' && attr !== false;
}

function AddJsonItem(data, name, value)
{
    let json = {name: name, value: value}
    data.push(json)
    return data
}

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


function RunAjax(url, method, data, call_type, other_info, onsuccess)
{

    var csrftoken = getCookie('csrftoken');

    var options =
        {
        url : url, // the endpoint
        type : method, // http method
        data : data, // data sent with the get request


        // handle a successful response
        success : function(json) {

            // j = $.parseJSON(json)
            //     $("#PersonId").val(j.PersonId)
            if (json.success)
            {
                console.log(json)
                console.log("success"); // another sanity check
                let msg = ""
                if (json.Message !== '')
                    msg = json.Message

                if (call_type === "UserSave") {
                    msg = "ذخیره اطلاعات کاربر با موفقیت انجام شد"
                    //fill all jobseeker and peron input

                    $("input[name='UserName']").val(json.username)
                    //show detail information
                    $(".UserDetail").show()
                    $(".TitleText").not(".Detail").click()
                }

                else if (call_type === "UserDetailDelete") {
                    msg = 'اطلاعات با موفقیت حذف شد'
                }
                if (msg!=''){
                $.alert({
                    title: 'موفقیت آمیز',
                    content: msg,
                    type: 'green',
                    typeAnimated: true,
                    buttons: {
                        close: {
                            text: 'بستن',
                            btnClass: 'btn-success',
                            action:function () {

                                //if we are in user page and insert mode, we must switch to update mode
                                if (typeof json.page != 'undefined') {
                                    if (json.page.name == 'person' && json.action_type == 'i') {
                                        location.replace('/HR/' + json.username)
                                    }
                                }
                            }
                        },
                    }
                })}
                if (call_type !== "UserSave")
                {
                    //in detail operation we must add or delete related record to/from table
                    //we have detail_type in data
                    let detail_type = json.detail_type[0];
                    let detail_id = json.id[0];

                    //remove current row
                    let table = $("#"+detail_type+"DetailTable");
                    table.find('tr[data-key="'+detail_id+'"]').remove();

                    switch (call_type)
                    {
                        //if we delete record from detail
                        case "UserDetailDelete":
                            break
                        //if we add new record to detail
                        case "UserDetailSave":
                            AddDetail(detail_type, json)
                            break
                    }

                }
                if (typeof onsuccess === 'function')
                    onsuccess()
            }
            else
            {

            $.alert({
                title: 'خطا',
                content: json.Message,
                type: 'red',
                typeAnimated: true,
                buttons: {
                    close: {
                        text: 'بستن',
                        btnClass: 'btn-success',
                    },
                }
            });
            }

        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {

            //alert(xhr.status + ' ' + xhr.responseText)
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
            //extract error info
            let rt =  xhr.responseText
            let ErrorText = ""
            let ErrorPlace = ""
            $(rt).find('tr th').each(
                function(index, item)
                {
                    if ($(item).text()==='Exception Value:')
                        ErrorText = $(item).next().text();
                    if ($(item).text()==='Exception Location:')
                        ErrorPlace = $(item).next().text();
                }
            );
            let msg = "";
            switch (call_type)
            {
                case "UserSave":
                    msg = "متاسفانه ذخیره اطلاعات کاربر با خطا مواجه شد";
                    break;

                case "UserDetailSave":
                    switch (data[data.length-1].value)
                    {
                        case "education":
                            msg = "ذخیره اطلاعات تحصیلی با خطا مواجه شد";
                            break;

                    }
                    break;
                default:
                    msg = "متاسفانه عملیات با خطا مواجه شد";
            }
            msg += "<br/>" +ErrorText+"<br/>"+ErrorPlace;
            $.alert({
                title: 'خطا',
                content: msg,
                type: 'red',
                typeAnimated: true,
                buttons: {
                    close: {
                        text: 'بستن',
                        btnClass: 'btn-red',
                    },
                }
            });
        }
    };
    var formData = new FormData();
    if ($('#avatar-file').length>0){


            data.forEach(function (item){
            formData.append(item.name,item.value);
        })
        formData.append('avatar-file',$('#avatar-file')[0].files[0]);
        options['data']=formData;
        options['async']=false;
        options['cache']= false;
        options['contentType']= false;
        options['enctype']= 'multipart/form-data';
        options['processData']= false;
        options ['headers']={
        'X-CSRFToken': csrftoken,
        };
    }
    if ($('#cv-file-up').length>0){


            data.forEach(function (item){
            formData.append(item.name,item.value);
        })
        formData.append('cv-file',$('#cv-file-up')[0].files[0]);
        options['data']=formData;
        options['async']=false;
        options['cache']= false;
        options['contentType']= false;
        options['enctype']= 'multipart/form-data';
        options['processData']= false;
        options ['headers']={
        'X-CSRFToken': csrftoken,
        };
    }
    console.log(options.data)
    $.ajax(options)
}
function AddDetail(detail_type, data)
{
    //find detail tabel
    let table = $("#"+detail_type+"DetailTable")
    let form = $("form[name='frm"+detail_type+"']")

    //remove existing row in update mode
    table.find('tr[data-key="'+data.id+'"]').remove()

    let tr = '<tr data-key="'+data.id+'">'
    table.find('th').each(
        function (index, item)
        {

            if (HasAttr(item,'data-field') && $(item).attr("data-field") !== '')
            {
                let field = $(item).attr("data-field")
                if (data.hasOwnProperty(field))
                {
                    let td = '<td>'
                    td += data[field]
                    td += '</td>'
                    tr += td
                }
            }
        }
    )

    //now add hidden td with all data
    let td = '<td class="hidden">'
    $.each(data, function(key,value)
    {
        td += '<input type="hidden" name="'+key+'" value="'+value[0]+'"/>'
    });
    tr += td + '</td>'

    //now add operation td
    let icon_edit = '<i class="fa-solid fa-edit icon edit"></i>'
    let icon_delete = '<i class="fa-solid fa-delete icon delete"></i>'
    let operation = '<td>'+icon_edit + icon_delete + '</td>'
    tr += operation

    //now close row
    tr += '</tr>'

    //add new row with new value
    table.find('tbody').append(tr)

    //now we must bind event for new icon
    table.find("tr[data-key='"+data.id+"'] .edit.icon").bind("click",
        function()
        {
            TableInfoEdit(this)
        }
    )
    table.find("tr[data-key='"+data.id+"'] .delete.icon").bind("click",
        function()
        {
            TableInfoDelete(this)
        }
    )

    //now reset form data
    RestFrom(form)
}


$(".detail").ready(
    function ()
    {
        $(".detail-fields form").each(
            function ()
            {

                RestFrom($(this))
            }
        )
    }
)
/******************************User List Function******************/

$(".cv-file").click(
    function ()
    {
        $("#cv-file-up").click()
    }
)


$(".pdatepicker").persianDatepicker({
            format: 'YYYY/MM/DD',
            calendar:{
                persian: {
                    leapYearMode: 'astronomical'
                }
        }

 });


function CascadeChange(Parent, Child)
{
    let p = Parent.val()
    Child.find("option").hide()
    Child.find(".p"+p).show()
    Child.val(0)
}
$("select.ParentCombo").change(
    function ()
    {
        debugger
        let parent = $(this)
        let children_name = $(this).attr("data-child")
        let children = parent.parentsUntil("form").find('select[name="'+children_name+'"]')
        CascadeChange(parent, children)
    }
)


$("#UniversityType").change(
    function ()
    {
        $("#Uni").val(0)
        ut = this.value
        c = $("#UniCity").val()
        $("#Uni option").hide()
        if (c != NaN && c > 0 && ut != NaN && ut > 0)
        {
            $("#Uni option.C_"+c+"_UT_"+ut).show()
        }
    }
)

/*************************Validator Start*************************/
function Validator(RecordType)
{

    function UsernameValidator(){
        let N = $("#user_name")
        let r = 0
        let username = N.val()
        let errmsg="<span class='ErrorMessage'>نام کاربری معتبر نیست</span>"

        const valid_username_regex=/^[a-zA-Z0-9_.-]+$/

        if (!valid_username_regex.test(username)){
            N.parent().before(errmsg)
            return -1;
        }
        return r
    }
    function NationalCodeValidator()
    {
        let N = $("#national_code")
        let code = N.val()
        let r = 0;
        let errmsg="<span class='ErrorMessage'>کد ملی معتبر نیست</span>"
        if (!isNaN(code) && code != "") {

            let L = code.length;

            if (L < 8 || parseInt(code, 10) == 0)
            {N.parent().before(errmsg)
                return -1;
            }
            code = ('0000' + code).substr(L + 4 - 10);
            if (parseInt(code.substr(3, 6), 10) == 0)
            {
               //debugger
                N.parent().before(errmsg)
                return -2;
            }
            var c = parseInt(code.substr(9, 1), 10);
            var s = 0;
            for (var i = 0; i < 9; i++)
                s += parseInt(code.substr(i, 1), 10) * (10 - i);
            s = s % 11;
            if (!((s < 2 && c == s) || (s >= 2 && c == (11 - s))))
            {
                //debugger
                 N.parent().before(errmsg)
                return  -3;
            }
        }
        return r
    }
    function ErrorMessage(element, msg)
    {
        $(element).parent().before("<p class='ErrorMessage'>"+msg+"</p>")
        $(element).addClass("ErrorBorder")
    }
    function RequiredFieldValidator(Fields, RecordType)
    {
        debugger
        function IsEmpty(value)
        {
            return value == '' || value == NaN || value == null || value == 0;
        }
        function RequiredField(Field)
        {
            let f =  $("form[name='frm"+RecordType+"'] [name='"+Field+"']")
            //date element is complex and contain 3 sub element day, month, year

            if (IsEmpty(f.val()))
            {
                f.parent().addClass("RequiredError")
                return -1;
            }
            return 0;
        }
        let e = 0;
        $.each(Fields,
            function (index, value)
            {
                e = RequiredField(value)
            })
        return e
    }
    function UserValidator()
    {
        let e = 0
        e += NationalCodeValidator()
        e += UsernameValidator()
        let m=$('#Military').val()
        let g = $('[name="Gender"]').val()
        if ((g = 0 && m!=='خانم ها'))
        e+= -1

        return e

    }
    function EducationHistoryValidator()
    {
        let StartYear=$('form[name="frmeducation"] input[name="StartYear"]').val()
        let EndYear=$('form[name="frmeducation"] input[name="EndYear"]').val()
        if (StartYear !== '' && EndYear !== '' &&  EndYear<StartYear)
            return -1
        return 0
    }

    function NumericValidator(RecordType)
    {
        let e = 0
        //check all numeric input with min/max value
        $("form[name='frm"+RecordType+ "']").find("input[type='number']").each(
            function(index, item)
            {
                //if item has value, check it
                if ($(item).val() != NaN && $(item).val() != null)
                {
                    if (HasAttr(item,"min") && parseInt($(item).attr("min")) > parseInt($(item).val()))
                    {
                        ErrorMessage(item, "مقدار بایستی بیشتر از "  + $(item).attr("min") + " باشد.")
                        e += -1
                    }
                    if (HasAttr(item,"max") && parseInt($(item).attr("max")) < parseInt($(item).val()))
                    {
                        ErrorMessage(item, "مقدار بایستی کمتر از "  + $(item).attr("max") + " باشد.")
                        e += -1
                    }

                }

            }
        )
        return e
    }


    $(".RequiredError").removeClass("RequiredError")
    $(".ErrorMessage").remove()
    $(".ErrorBorder").removeClass("ErrorBorder")
    let e = 0;

    let RequiredFields = []
    let Fields = $("form[name='frm"+RecordType+"'] .Required")
    // Fields +=
     $.each(Fields,
         function (){
           RequiredFields.push($(this).attr('for'))
         })


    switch (RecordType)
    {
        case "person":
            //set required fields

            e += UserValidator()
            break;
        case "education":

            e +=  EducationHistoryValidator()
            break


        case "PhoneNumber":

            break
        case "PostalAddress":

            break
    }
    //check required fields
    e += RequiredFieldValidator(RequiredFields,RecordType)
    e += NumericValidator(RecordType)
    return e

}
/*************************Validator End*************************/

/**********************Detail Information Start********************/
function Save(SaveIcon)
{
    debugger
    let detail_type = $(SaveIcon).attr("data-type")
    let data = {}
    let url = ''
    let call_type = ''
    let e = 0
    e = 0
    e = Validator(detail_type)
    let Form = $("form[name='frm"+detail_type+"']")

    if (e >= 0)
    {
        //if select item is null, it would be deleted from serialization action
        //so, we found all null value select item
        Form.find('select').each(
            function()
            {
                if ($(this).val() == null || $(this).val() === undefined)
                    $(this).val(0)
            }
        )
        data = Form.serializeArray();
        if (detail_type == "person")
        {
            call_type = "UserSave"
            let username = Form.find('input[name="username"]').val()
            //if this filed already exists it mean that we are in edit mode
            if (username !== '')
                url = "/HR/save/u"
            else
                url = "/HR/save/i"
        }
        else
        {
            let id = Form.find("input[name='"+detail_type+"Id']").val()

            data = AddJsonItem(data, 'id',id)
            data = AddJsonItem(data, 'detail_type',detail_type)
            url = "/HR/detail/save"
            call_type = "UserDetailSave"
        }

        RunAjax(url, "POST", data, call_type)
    }
    else {
        $.alert({
            title: 'خطا',
            content: 'امکان ذخیره داده ها وجود ندارد. لطفاً خطاهای موجود را تصحیح کنید',
            type: 'red',
            typeAnimated: true,
            buttons: {
                close: {
                    text: 'بستن',
                    btnClass: 'btn-red',
                },
            }
        });
    }
    return e;

}

function RestFrom(form)
{
    //call reset form button
    form.find('button[type="reset"]').click()

    //reset all combo
    form.find('select.ParentCombo').each(
        function(index, item)
        {
            $(item).val(0)
            //for parent combo we must hide child combo
            if (HasAttr(item, 'data-child'))
            {
                let child = $(item).attr('data-child')
                //now find children combo and hide items
                form.find('select[name="'+child+'"] option').hide()
                form.find('select[name="'+child+'"] option[value=0]').show()
            }
        }
    )
}

$(".button.save").click(
    function()
    {
       //debugger
        Save(this)
    }
)
$('.icon.add').click(function()
{
    // debugger
    let detail = $(this).next(".detail-fields")
    detail.animate({
    height: [ "toggle", "swing" ],

  }, 1000, "linear")
    // if (detail.height() > 1)
    // {
    //     detail.animate({height: '1px'}, 1000)
    // }
    // else
    // {
    //     detail.animate({height: '100%'}, 1000)
    //
    // }

})
function TableInfoEdit(icon)
{
  //we must copy all data to related form in bottom of table
        //all data of this record is saved in hidden input which are in previous td
        //,so we find previous td first
        let td = $(icon).parent().prev()
        let detail_type = $(icon).attr("data-type")
        //at first, we must find form name
        let form_name = "frm" + detail_type
        let frm = $("form[name='"+form_name+"']")
        // now for each input of in this row, we must fill related input in form
        td.find("input").each(
            function (index, item) {
                //read data from hidden input
                let name = $(item).attr("name")
                let value = $(item).val()
                //fill data in related input in form
                frm.find("input[name='"+name+"']").val(value)
                frm.find("select[name='"+name+"']").val(value)
                if ($(item).prop('checked'))
                    frm.find("input[name='"+name+"']").prop('checked',true)

            }
        )
}
function TableInfoDelete(icon)
{
    let id = $(icon).parents('tr').attr('data-key')
    let detail_type = $(icon).attr("data-type")
    let crf_token = $("input[name='csrfmiddlewaretoken']").val()
    let data = {"id": id, "detail_type":detail_type, "csrfmiddlewaretoken":crf_token }
    RunAjax("/HR/detail/delete", "POST", data, "UserDetailDelete")
}
$(".detail .icon.edit").click(
    function ()
    {
        debugger
        //open detail information div
        let detail =  $(this).parents('fieldset').find('.detail-fields')
        detail.show(function () {
            detail.animate({height: "100%"}, 1000, "linear")
        })

        TableInfoEdit(this)
    }
)
$(".detail .icon.delete").click(
    function () {

        let detail = $(this).parents('table.detail').nextAll('.detail-fields')
        let icon = this
        let detail_type = $(this).attr('data-type')
        let form = $('form[name="frm'+detail_type+'"]')
        $.confirm({
            title: 'تایید حذف',
            content: 'آیا از حذف این رکورد اطمینان دارید؟',
            buttons: {
                confirm: {
                    text: 'حذف شود',
                    btnClass: 'btn-red',
                    action:function ()
                    {

                        RestFrom(form)
                        TableInfoDelete(icon)
                        detail.animate({height: "0"}, 1000, "linear",
                            function ()
                            {
                                detail.hide()
                            })
                    }

                },
                cancel:  {
                    text: 'انصراف',
                    btnClass: 'btn-blue',
                },
            }
        })

    }
)
/**********************Detail Information Start********************/

/******************************************Menu Start***************************************/
$('.panel-menu').click(
    function (){
        if (!$(this).hasClass('disabled')){
            $('.info-panel').addClass('hidden')
            var infopanel = $(this).attr('data')
            $('.'+infopanel).removeClass('hidden')
        }
        else{
            $.alert('لطفا ابتدا اطلاعات کاربر را ثبت نمایید')
        }
    }
)
$(".logo").click(
    function ( )
    {
          $('.logo').not('.logogray').each(
              function (index, item)
              {
                  filepath = $(item).attr('src')
                  filepath = filepath.substring(0, filepath.length - 4) //remove .png
                  filepath = filepath + '-Gray.png'
                  $(item).attr('src',filepath)
              }
          )
          $('.logo').not('.logogray').addClass('logogray')



        if ($(this).hasClass('logogray'))
        {
          filepath = $(this).attr('src')
            //replace with hover image
          filepath = filepath.substring(0, filepath.length - 9) //remove .png
          filepath = filepath + '.png'

          $(this).attr('src',filepath)
          $(this).removeClass('logogray')
        }
    }
)

/******************************************Menu End***************************************/
/******************************************personeli Start******************************************/
$('form[name="frmperson"] .Save').click(
    function (){
        $('.panel-menu').removeClass('disabled')
    }
)
$('form[name="frmperson"] select[name="team"]').change(
    function ()
    {

        //check which roles are valid for this team
        let valid_role = $(this).find('option:selected').attr('data-target')
        valid_role = JSON.parse(valid_role)
        //hide all roles
        let roles_combo = $('form[name="frmperson"] select[name="role"]')
        roles_combo.val(0)
        $('form[name="frmperson"] select[name="level"]').val(0)
        roles_combo.find('option').hide()
        $.each(valid_role,
            function (index, item) {
                //show this role
                roles_combo.find('option[value="'+item+'"]').show()
            }
        )
    })
$('form[name="frmperson"] select[name="role"]').change(
    function ()
    {

        //get selected value
        let val = $(this).val()
        //check if selected role has level
        let selected_option = $(this).find('option[value="'+val+'"]')
        //find level combo label and div
        let level_div = $('form[name="frmperson"] select[name="level"]').parent('div')
        let level_label = $('form[name="frmperson"] label[for="level"]')
        level_div.find('select').val(0)
        if (selected_option.hasClass("has_level"))
        {
            // show role item
            level_div.show()
            level_label.addClass('Required')
        }
        else
        {
            level_div.hide()
            level_label.removeClass('Required')
        }
})


/******************************************personeli End******************************************/
/******************************************list Start******************************************/
$('.tr-href').on('click',function(){
   var url = $(this).attr('data-href');
   window.location.href = url;
})


$('.search_icon').on('click',function(){
    var txtname = $(this).val();
    var txtlastname = $(this).val();
    var valname = $(this).val();
    var valname = $(this).val();
    var valname = $(this).val();
    $('.item').removeClass('d-none');
    $('.item').each(function(){
        var name = $(this).attr('data-value');
        if (!name.includes(val)){
            $(this).addClass('d-none');
        }
    });
})

function search(input, td)
{
    let val = input.val()
    if (val != '')
    {
        $('.tr-href').hide()
        $('.' + td + '[data-value^="'+val+'"]').parent().show()
    }
    else
        $('.tr-href').show()

}

var persian_char =  /^[\u0600-\u06FF\s]+$/;
$(document).on('keydown',".search_x",function(event){
    var elm = $(this);
    if(persian_char.test(event.key)){
        if(event.key == 'ی'){
            event.preventDefault();
            event.stopPropagation();
            elm.val(elm.val()+"ي")
        }
    }


})


$('input').keyup(
    function ()
    {
        // search($(this), $(this).attr("data-value"))
         $('.tr-href').hide()
         $('.tr-href').css("background-color","unset");
        let name =  ($('#txt-name').val()) ? '[data-value*="' +  $('#txt-name').val() + '"]':''
        let last_name =  ( $('#txt-lastname').val()) ? '[data-value*="' +   $('#txt-lastname').val() + '"]':''
        let team =  ( $('#txt-team').val()) ? '[data-value*="' +   $('#txt-team').val() + '"]':''
        let role =  ( $('#txt-role').val()) ? '[data-value*="' +   $('#txt-role').val() + '"]':''
        let username =  ( $('#txt-username').val()) ? '[data-value*="' +   $('#txt-username').val() + '"]':''

        $('.item-name'+name).parent().find('.item-username'+username).parent().find('.item-lastname'+last_name).parent().find('.item-team'+team).parent().find('.item-role'+role).parent().show()
         //$('.tr-href:visible:nth-child(odd)').css("background-color","red")
        $('.tr-href').not('[style*="display: none;"]').each(function(index,item){
                if(index % 2 == 0){
                    $(this).css("background-color","#c3dda4");
                }

        });


        // $('.tr-href').each(
        //     function(index, item)
        //     {
        //
        //
        //     }
        // )
    }
)

/******************************************lis End******************************************/
/********************************user History start***************************/
$('.gender_logo').click(
    function ()
    {
        $('.gender_logo').removeClass('active')
        $(this).addClass('active')
        $('input[name="gender"]').val($(this).attr('value'))
    }
)
/********************************user History end***************************/
/********************************user personeli start***************************/

$('.Avatar').click(function (){
    $('#avatar-file').trigger('click')
});

setTimeout(function (){
   $('[name="frmperson"]').attr('enctype','multipart/form-data')
   $('[name="frmperson"]').attr('method','post')
},500);

/*************************Hi chart Start*****************************************/
// Data retrieved https://en.wikipedia.org/wiki/List_of_cities_by_average_temperature
// Highcharts.chart('container', {
//   chart: {
//     type: 'spline'
//   },
//   title: {
//     text: 'پرداختی فرد'
//   },
//   subtitle: {
//     text: 'در طول سال'
//   },
//   xAxis: {
//     categories: ['فروردین', 'اردیبهشت', 'خرداد', 'تیر', 'مرداد', 'شهریور',
//       'مهر', 'آبان', 'آذر', 'دی', 'بهمن', 'اسفند'],
//     accessibility: {
//       description: 'ماه های سال'
//     }
//   },
//   yAxis: {
//     title: {
//       text: 'مبلغ به تومان'
//     },
//     labels: {
//       formatter: function () {
//         return this.value + 'تومان';
//       }
//     }
//   },
//   tooltip: {
//     crosshairs: true,
//     shared: true
//   },
//   plotOptions: {
//     spline: {
//       marker: {
//         radius: 4,
//         lineColor: '#666666',
//         lineWidth: 1
//       }
//     }
//   },
//   series: [{
//     name: 'پرداختی',
//     marker: {
//       symbol: 'square'
//     },
//     data: [200000, 250000, 300000, 320000, 350000, 360000, 380000, {
//       y: 390000,
//       marker: {
//         symbol: 'url(/static/HR/images/icon/sun.png)'
//       },
//       accessibility: {
//         description: 'این بیشترین مبلغ دریافتی بوده است'
//       }
//     }, 380000, 370000, 360000, 350000]
//
//   }, {
//     name: 'پاداش',
//     marker: {
//       symbol: 'diamond'
//     },
//     data: [{
//       y: 200000,
//       marker: {
//         symbol: 'url(/static/HR/images/icon/snow.png)'
//       },
//       accessibility: {
//         description: 'این کمترین مقدار بازگشتی بوده است'
//       }
//     }, 300000, 310000, 320000, 300000, 290000, 310000, 320000, 330000, 280000, 270000, 260000]
//   }]
// });
//
function draw_chart(chart_id,title,subtitle, xAxis, series) {

    Highcharts.chart(chart_id, {
          chart: { type: 'spline',},
          title: { text: title  },
          subtitle: { text: subtitle},
          xAxis: {
            categories: xAxis,
            accessibility: {
              description: 'ماه های سال'
            }
          },
          yAxis: {
            title: {
              text: 'مبلغ به تومان',
            },
            labels: {
              formatter: function () {
                return this.value + 'تومان';
              }
            }
          },
          tooltip: {
            crosshairs: true,
            shared: true
          },
          plotOptions: {
            spline: {
              marker: {
               enabled: false
              }
            }
          },
          series: series,
          navigation: {
              menuItemStyle: {
                  fontSize: '10px',
              }
          }
    })

}
/*
data = [
                ['Chrome', 73.86],
                ['Edge', 11.97],
                ['Firefox', 5.52],
                ['Safari', 2.98],
                ['Internet Explorer', 1.90],
                {
                    name: 'Other',
                    y: 3.77,
                    dataLabels: {
                        enabled: false
                    }
                }
            ]
*/
 function draw_pie_chart(chart_id, title, subtitle, data)
{
    Highcharts.chart(chart_id, {
        chart: {
            plotBackgroundColor: null,
            plotBorderWidth: 0,
            plotShadow: false
        },
        title: {
            text: title,
            align: 'center',
            verticalAlign: 'middle',
            y: 60
        },
        tooltip: {
            pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
        },
        accessibility: {
            point: {
                valueSuffix: '%'
            }
        },
        plotOptions: {
            pie: {
                dataLabels: {
                    enabled: true,
                    distance: -50,
                    style: {
                        fontWeight: 'bold',
                        color: 'white'
                    }
                },
                startAngle: -90,
                endAngle: 90,
                center: ['50%', '75%'],
                size: '110%'
            }
        },
        series: [{
            type: 'pie',
            name: subtitle,
            innerSize: '50%',
            data: data
        }]
    });
}
function  draw_column_chart(chart_id, title, subtitle, categories, series)
{
Highcharts.chart(chart_id, {
    chart: {
        type: 'column'
    },
    title: {
        text: title
    },
    subtitle: {
        text: subtitle
    },
    xAxis: {
        categories: categories,
        crosshair: true
    },
    yAxis: {
        min: 0,
        title: {
            text: 'هزینه ها'
        }
    },
    tooltip: {
        headerFormat: '<span style="font-size:10px">{point.key}</span><table>',
        pointFormat: '<tr><td style="color:{series.color};padding:0">{series.name}: </td>' +
            '<td style="padding:0"><b>{point.y:.1f} تومان</b></td></tr>',
        footerFormat: '</table>',
        shared: true,
        useHTML: true
    },
    plotOptions: {
        column: {
            pointPadding: 0.2,
            borderWidth: 0
        }
    },
    series: series
});
}
$('.payment-page .filter .top span').click(
    function ()
    {
        if ($(this).parent().hasClass('years'))
            //سال مربوطه را در input سال قرار می دهیم
            $('.payment-page form[name="chart_data"] input[name="year_number"]').val($(this).text())
        else
        {
            $('.payment-page form[name="chart_data"] input[name="role_id"]').val($(this).data('key'))
            $('.payment-page form[name="chart_data"] input[name="role_title"]').val($(this).text())

        }

        //اکنون فرم را با داده های جدید ارسال می کنیم تا صفحه رفرش شود
        $('.payment-page form[name="chart_data"]').submit()
        // //کلاس فعال را از همه سالها بر می داریم
        // $(this).parent().find('span').removeClass('active')
        // // کلاس فعال را برای این سال می گذاریم
        // $(this).addClass('active')

    }
)
function get_input_list(list_name, page_name)
{
    let list = $('.'+page_name+' input[name="'+list_name+'"]').val()
    if (list.length > 1)
        return JSON.parse(list)
    return ''
}
function get_string_input_list(list_name, page_name)
{
    let list = $('.'+page_name+' input[name="'+list_name+'"]').val()
    list = list.replace('[', '').replace(']', '')
    list = list.replaceAll("(", "").replaceAll(",)", "")
    list = list.replaceAll("'", "")
    list = list.replace(">", "")
    list = list.replace("<QuerySet ", "")
    list = list.split(',')
    return list
}
$('.payment-page .filter .menu span').click(
    function () {
        let more_payment_count = parseInt($('.payment-page input[name="more_payment_count"]').val())
        let less_payment_count = parseInt($('.payment-page input[name="less_payment_count"]').val())
        let more_role_payment_count = parseInt($('.payment-page input[name="more_role_payment_count"]').val())
        let less_role_payment_count = parseInt($('.payment-page input[name="less_role_payment_count"]').val())


        let payment_average_payment = get_input_list("payment_average_payment", 'payment-page')
        let payment_average_base_payment = get_input_list("payment_average_base_payment", 'payment-page')
        let payment_average_other_payment = get_input_list("payment_average_other_payment", 'payment-page')
        let payment_average_over_time_payment = get_input_list("payment_average_over_time_payment", "payment-page")
        let payment_average_reward = get_input_list("payment_average_reward", "payment-page")

        let role_payment_average_payment = get_input_list("role_payment_average_payment", "payment-page")
        let role_payment_average_base_payment = get_input_list("role_payment_average_base_payment", "payment-page")
        let role_payment_average_other_payment = get_input_list("role_payment_average_other_payment", "payment-page")
        let role_payment_average_over_time_payment = get_input_list("role_payment_average_over_time_payment", "payment-page")
        let role_payment_average_reward = get_input_list("role_payment_average_reward", "payment-page")

        let person_payment_payment = get_input_list("person_payment_payment", "payment-page")
        let person_payment_base_payment = get_input_list("person_payment_base_payment", "payment-page")
        let person_payment_other_payment = get_input_list("person_payment_other_payment", "payment-page")
        let person_payment_over_time_payment = get_input_list("person_payment_over_time_payment", "payment-page")
        let person_payment_reward = get_input_list("person_payment_reward", "payment-page")

        let person_all_year_payment = get_input_list("person_all_year_payment", "payment-page")
        let person_all_year_base_payment = get_input_list("person_all_year_base_payment", "payment-page")
        let person_all_year_average_payment = get_input_list("person_all_year_average_payment", "payment-page")
        let person_all_year_average_role_payment = get_input_list("person_all_year_average_role_payment", "payment-page")

        let role_id = $('.payment-page input[name="role_id"]').val()

        let year_number = $('.payment-page input[name="year_number"]').val()
        let subtitle = 'در طول سال ' + year_number

        let month_name = get_string_input_list('month_name', "payment-page")
        let year_list = get_string_input_list('year_list', "payment-page")

        // منوی کلیک شده را فعال می کنیم
        $(this).parent().find('span').removeClass('active')
        $(this).addClass('active')

        //اطلاعات منوی فعال را در input مربوطه ذخیره می کنیم که وقتی صفحه رفرش می شود همین منو فعال باشد
        let chart_type = $(this).data('key')

        //اگر روی فیلتر سال یا سمت کلیک کرده باشد نوع خالی است
        //باید نوع را از مقدار قبلی به دست بیاوریم
        if (chart_type == undefined || chart_type == NaN || chart_type == 'undefined')
           chart_type = $('.payment-page form[name="chart_data"] input[name="current_chart"]').val()
        else
            $('.payment-page form[name="chart_data"] input[name="current_chart"]').val(chart_type)

        //اگر منوی جاری مربوط به تمامی سالها باشد فیلتر سال را حذف می کنیم
        if (chart_type=='person-all-year-payment-chart')
            $('.filter .years').hide()
        else
            $('.filter .years').show()

        let data = []

        $('.payment-page figure').hide()

        $('#'+chart_type).parent().show()
        let series = []
        switch (chart_type) {
            case 'payment-count-chart':
                    data = [['افرادی با حقوق بیشتر',more_payment_count],['افرادی با حقوق کمتر',less_payment_count]]
                    draw_pie_chart('payment-count-chart', 'جایگاه حقوق فرد','در شرکت', data)
                break
            case 'role-payment-count-chart':
                    data = [['افرادی با حقوق بیشتر',more_role_payment_count],['افرادی با حقوق کمتر',less_role_payment_count]]
                    draw_pie_chart('role-payment-count-chart', 'جایگاه حقوق فرد', 'در افرادی با سمت مشابه', data)
                break
            case 'person-all-year-payment-chart':
                series = [{name: 'خالص دریافتی', data: person_all_year_payment},
                            {name: 'مبلغ حکم', data: person_all_year_base_payment},
                            {name: 'میانگین دریافتی شرکت', data: person_all_year_average_payment},
                            {name: 'میانگین دریافتی این سمت', data: person_all_year_average_role_payment},
                ]
                draw_chart('person-all-year-payment-chart', 'پرداختی هر فرد', 'در طول سالها', year_list, series)
                break
            case 'person-yearly-payment-chart':
                series = [{name: 'خالص دریافتی', data: person_payment_payment},
                            {name: 'مبلغ حکم', data: person_payment_base_payment},
                            {name: 'میانگین دریافتی شرکت', data: payment_average_payment},
                            {name: 'میانگین دریافتی این سمت', data: role_payment_average_payment},
                ]
                draw_chart('person-yearly-payment-chart', 'پرداختی هر فرد', subtitle, month_name, series)
                break

            case 'other-payment-yearly-chart':
                series = [
                    {name: 'سایر هزینه ها', data: person_payment_other_payment},
                    {name: 'میانگین سایر هزینه ها در شرکت', data: payment_average_other_payment},
                    {name: 'میانگین سایر هزینه ها برای این سمت در شرکت', data: role_payment_average_other_payment},
                ]
                draw_chart('other-payment-yearly-chart', 'سایر پرداختی های هر فرد', subtitle, month_name, series)
                break

            case 'over-time-yearly-chart':
                series = [
                    {name: 'اضافه کار', data: person_payment_over_time_payment},
                    {name: 'میانگین اضافه کار در شرکت', data: payment_average_over_time_payment},
                    {name: 'میانگین اضافه کار این سمت در شرکت', data: role_payment_average_over_time_payment},
                ]
                draw_chart('over-time-yearly-chart', 'مبلغ اضافه کاری', subtitle, month_name, series)
                break

            case 'reward-yearly-chart':
                series = [
                    {name: 'پاداش',data: person_payment_reward},
                    {name: 'میانگین پاداش در شرکت',data: payment_average_reward},
                    {name: 'میانگین پاداش این سمت در شرکت',data: role_payment_average_reward},
                ]
                draw_chart('reward-yearly-chart', 'پاداش های دریافتی', subtitle, month_name, series)
                break

       }


    }
)
$('.payment-page form[name="chart_data"]').ready(
    function () {
        //نمودار فعلی را به دست می آوریم
        let current_chart = $(this).find('input[name="current_chart"]').val()
        // این تابع را فراخوانی می کنیم تا نمودار جاری را نمایش دهد
        $('.payment-page .filter .navigation span[data-key="'+current_chart+'"]').click()
    }
)
$('.facilities-page .filter .top span').click(
    function ()
    {
        //سال مربوطه را در input سال قرار می دهیم
        $('.facilities-page form[name="chart_data"] input[name="year_number"]').val($(this).text())
        //اکنون فرم را با داده های جدید ارسال می کنیم تا صفحه رفرش شود
        $('.facilities-page form[name="chart_data"]').submit()
        // //کلاس فعال را از همه سالها بر می داریم
        // $(this).parent().find('span').removeClass('active')
        // // کلاس فعال را برای این سال می گذاریم
        // $(this).addClass('active')

    }
)
$('.facilities-page form[name="chart_data"]').ready(
    function () {
        //نمودار فعلی را به دست می آوریم
        let current_chart = $(this).find('input[name="current_chart"]').val()
        // این تابع را فراخوانی می کنیم تا نمودار جاری را نمایش دهد
        $('.facilities-page .filter .navigation span[data-key="'+current_chart+'"]').click()
    }
)

$('.facilities-page .filter .navigation span').click(
    function () {
        let nahar_time_EIT = get_input_list("nahar_time_EIT", "facilities-page")
        let nahar_time_user = get_input_list("nahar_time_user", "facilities-page")
        let month_name_nahar_time = get_string_input_list('month_name_nahar_time', "facilities-page")

        let nahar_time_average_EIT = get_input_list("nahar_time_average_EIT", "facilities-page")
        let nahar_time_average_user = get_input_list("nahar_time_average_user", "facilities-page")
        let month_name_nahar_time_average = get_string_input_list('month_name_nahar_time_average', "facilities-page")

        let insurance_cost_EIT = get_input_list("insurance_cost_EIT", "facilities-page")
        let insurance_cost_user = get_input_list("insurance_cost_user", "facilities-page")
        let month_name_insurance_cost = get_string_input_list('month_name_insurance_cost', "facilities-page")

        let insurance_cost_average_EIT = get_input_list("insurance_cost_average_EIT", "facilities-page")
        let insurance_cost_average_user = get_input_list("insurance_cost_average_user", "facilities-page")
        let month_name_insurance_average_cost = get_string_input_list('month_name_insurance_average_cost', "facilities-page")

        let role_id = $('.facilities-page input[name="role_id"]').val()

        let year_number = $('.facilities-page input[name="year_number"]').val()
        let subtitle = 'در طول سال ' + year_number

        let year_list = get_string_input_list('year_list', "facilities-page")

        // منوی کلیک شده را فعال می کنیم
        $(this).parent().find('span').removeClass('active')
        $(this).addClass('active')

        //اطلاعات منوی فعال را در input مربوطه ذخیره می کنیم که وقتی صفحه رفرش می شود همین منو فعال باشد
        let chart_type = $(this).data('key')
        $('.facilities-page form[name="chart_data"] input[name="current_chart"]').val(chart_type)
        //اگر منوی جاری مربوط به تمامی سالها باشد فیلتر سال را حذف می کنیم
        if (chart_type=='person-all-year-payment-chart')
            $('.filter .years').hide()
        else
            $('.filter .years').show()


        $('.facilities-page figure').hide()

        $('#'+chart_type).parent().show()
        let series = []
        switch (chart_type) {
            case 'nahar-time-chart':
                $('#nahar-time-chart').parent().show()
                series = [{name: 'پرداختی فرد', data: nahar_time_user},
                            {name: 'پرداختی شرکت', data: nahar_time_EIT},
                ]
                draw_column_chart('nahar-time-chart', 'ناهار تایم', subtitle, month_name_nahar_time, series)

                $('#nahar-time-average-chart').parent().show()
                series = [{name: 'پرداختی فرد', data: nahar_time_average_user},
                            {name: 'پرداختی شرکت', data: nahar_time_average_EIT},
                ]
                draw_column_chart('nahar-time-average-chart', 'ناهار تایم', subtitle, month_name_nahar_time_average, series)

                break
            case 'insurance-cost-chart':
                $('#insurance-cost-chart').parent().show()
                series = [{name: 'پرداختی فرد', data: insurance_cost_user},
                            {name: 'پرداختی شرکت', data: insurance_cost_EIT},
                ]
                draw_column_chart('insurance-cost-chart', 'بیمه تکمیل درمان', subtitle, month_name_insurance_cost, series)

                $('#insurance-cost-average-chart').parent().show()
                series = [{name: 'پرداختی فرد', data: insurance_cost_average_user},
                            {name: 'پرداختی شرکت', data: insurance_cost_average_EIT},
                ]
                draw_column_chart('insurance-cost-average-chart', 'بیمه تکمیل درمان', subtitle, month_name_insurance_average_cost, series)
                break

       }
    })



//
// Highcharts.chart('container', {
//     chart: {
//         type: 'spline',
//         scrollablePlotArea: {
//             minWidth: 600,
//             scrollPositionX: 1
//         }
//     },
//
//     xAxis: {
//         type: 'int',
//         labels: {
//             overflow: 'justify'
//         }
//     },
//     yAxis: {
//         title: {
//             text: 'مبلغ'
//         },
//         minorGridLineWidth: 0,
//         gridLineWidth: 0,
//         alternateGridColor: null,
//         plotBands: [{ // Light air
//             from: 0.3,
//             to: 1.5,
//             color: 'rgba(68, 170, 213, 0.1)',
//             label: {
//                 text: 'Light air',
//                 style: {
//                     color: '#606060'
//                 }
//             }
//         }, { // Light breeze
//             from: 1.5,
//             to: 3.3,
//             color: 'rgba(0, 0, 0, 0)',
//             label: {
//                 text: 'Light breeze',
//                 style: {
//                     color: '#606060'
//                 }
//             }
//         }, { // Gentle breeze
//             from: 3.3,
//             to: 5.5,
//             color: 'rgba(68, 170, 213, 0.1)',
//             label: {
//                 text: 'Gentle breeze',
//                 style: {
//                     color: '#606060'
//                 }
//             }
//         }, { // Moderate breeze
//             from: 5.5,
//             to: 8,
//             color: 'rgba(0, 0, 0, 0)',
//             label: {
//                 text: 'Moderate breeze',
//                 style: {
//                     color: '#606060'
//                 }
//             }
//         }, { // Fresh breeze
//             from: 8,
//             to: 11,
//             color: 'rgba(68, 170, 213, 0.1)',
//             label: {
//                 text: 'Fresh breeze',
//                 style: {
//                     color: '#606060'
//                 }
//             }
//         }, { // Strong breeze
//             from: 11,
//             to: 14,
//             color: 'rgba(0, 0, 0, 0)',
//             label: {
//                 text: 'Strong breeze',
//                 style: {
//                     color: '#606060'
//                 }
//             }
//         }, { // High wind
//             from: 14,
//             to: 15,
//             color: 'rgba(68, 170, 213, 0.1)',
//             label: {
//                 text: 'High wind',
//                 style: {
//                     color: '#606060'
//                 }
//             }
//         }]
//     },
//     tooltip: {
//         valueSuffix: 'تومان'
//     },
//     plotOptions: {
//         spline: {
//             lineWidth: 4,
//             states: {
//                 hover: {
//                     lineWidth: 5
//                 }
//             },
//             marker: {
//                 enabled: false
//             },
//             pointInterval: 3600000, // one hour
//             pointStart: Date.UTC(2022, 5, 13, 0, 0, 0)
//         }
//     },
//           series: [
//                     {
//                         name: 'خالص دریافتی',
//                         marker: {symbol: 'square'},
//                         data: payment
//                     },
//                     {
//                         name: 'حقوق ناخالص',
//                         marker: {symbol: 'square'},
//                         data: total_payment
//                     },
//                     {
//                         name: 'سایر پرداختی ها',
//                         marker: {symbol: 'square'},
//                         data: other_payment
//                     },
//                     {
//                         name: 'اضافه کار',
//                         marker: {symbol: 'square'},
//                         data: over_time_payment
//                     },
//                     {
//                         name: 'پاداش',
//                         marker: {symbol: 'square'},
//                         data: reward
//                     },]
//     navigation: {
//         menuItemStyle: {
//             fontSize: '10px'
//         }
//     }
// });



/*************************Hi chart end*****************************************/