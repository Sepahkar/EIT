//*******************************General**************************
function ChangeImage(img, old_name, new_name)
{
    let s = img.attr("src")
    s = s.replace(old_name,new_name)
    img.attr("src",s)
}

function ChangeHoverImage(img, InOut)
{

    let filepath;
    if (InOut === "I") //Mouse over
    {
        filepath = $(img).attr('src')
        //replace with hover image
        filepath = filepath.substring(0, filepath.length - 4)//remove .png
        filepath = filepath + '-hover.png'
        $(img).attr('src', filepath)
    } else // Mouse out
    {
        filepath = $(img).attr('src')
        //replace with hover image
        filepath = filepath.substring(0, filepath.length - 10)//remove -hover.png
        filepath = filepath + '.png'
        $(img).attr('src', filepath)

    }

}

function RunAjax(url, method, data, call_type, other_info)
{
    debugger
    $.ajax(
        {
        url : url, // the endpoint
        type : method, // http method
        data : data, // data sent with the get request

        // handle a successful response
        success : function(json) {
            debugger
            // j = $.parseJSON(json)
            //     $("#PersonId").val(j.PersonId)
            if (json.success)
            {
                console.log(json)
                console.log("success"); // another sanity check
                let msg = ""
                switch (call_type)
                {
                    case "JobSeekerSave":
                        msg = "ذخیره اطلاعات کارجو با موفقیت انجام شد"
                        //fill all jobseeker and peron input
                        $("input[name='JobSeekerId']").val(json.JobSeekerId)
                        $("input[name='PersonId']").val(json.PersonId)
                        //show detail information
                        $(".JobSeekerDetail").show()
                        $(".TitleText").not(".Detail").click()
                        break
                    case "JobSeekerDetailDelete":
                        msg = "حذف اطلاعات با موفقیت انجام شد"
                        UpdateDetailTable(call_type, json.detail_type[0], json)
                        break
                    case "JobSeekerDetailSave":
                        switch (json.detail_type[0])
                        {
                            case "EducationHistory":
                                msg = "اطلاعات تحصیلی با موفقیت ذخیره شد"
                                break;
                            case "JobHistory":
                                msg = "اطلاعات سابقه شغلی با موفقیت ذخیره شد"
                                break;
                            case "PreferredCity":
                                msg = "اطلاعات شهرهای ترجیحی با موفقیت ذخیره شد"
                                break
                            case "PreferredJob":
                                msg = "اطلاعات شغلهای ترجیحی با موفقیت ذخیره شد"
                                break
                            case "JobSeekerSkill":
                                msg = "اطلاعات مهارتهای کارجو با موفقیت ذخیره شد"
                                break
                            case "Certification":
                                msg = "اطلاعات دوره های آموزشی با موفقیت ذخیره شد"
                                break
                            case "EmailAddress":
                                msg = "اطلاعات پست های الکترونیکی با موفقیت ذخیره شد"
                                break
                            case "PhoneNumber":
                                msg = "اطلاعات شماره های تماس با موفقیت ذخیره شد"
                                break
                            case "PostalAddress":
                                msg = "اطلاعات آدرس های پستی با موفیت ذخیره شد"
                                break
                        }
                        UpdateDetailTable(call_type, json.detail_type[0], json)
                        break
                    default:
                        msg = "عملیات موفقیت آمیز بود"
                }

                $.alert({
                    title: 'موفقیت آمیز',
                    content: msg,
                    type: 'green',
                    typeAnimated: true,
                    buttons: {
                        close: {
                            text: 'بستن',
                            btnClass: 'btn-success',
                        },
                    }
                });
                //in detail operation we must add or delete related record to/from table
                //we have detail_type in data
                let detail_type = data.detail_type
                let detail_id = data.id
                switch (call_type)
                {
                    //if we delete record from detail
                    case "JobSeekerDetailDelete":
                        $("tr."+detail_type+"[data='"+detail_id+"']").remove()
                        break
                    //if we add new record to detail
                    case "JobSeekerDetailAdd":
                        break
                }
            }
            else
            {
            $.alert({
                title: 'خطا',
                content: "ذخیره داده ها با خطا مواجه شد",
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
            //debugger
            //alert(xhr.status + ' ' + xhr.responseText)
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
            //extract error info
            let rt =  xhr.responseText
            let ErrorText = ""
            let ErrorPlace = ""
            $(rt).find('tr th').each(
                function(index, item)
                {
                    if ($(item).text()=='Exception Value:')
                        ErrorText = $(item).next().text()
                    if ($(item).text()=='Exception Location:')
                        ErrorPlace = $(item).next().text()
                }
            )
            let msg = ""
            switch (call_type)
            {
                case "JobSeekerSave":
                    msg = "متاسفانه ذخیره اطلاعات کارجو با خطا مواجه شد"
                    break
                case "JobSeekerDetailDelete":
                    msg = "متاسفانه حذف اطلاعات با خطا مواجه شد"
                    break
                case "JobSeekerDetailSave":
                    switch (data[data.length-1].value)
                    {
                        case "EducationHistory":
                            msg = "ذخیره اطلاعات تحصیلی با خطا مواجه شد"
                            break;
                        case "JobHistory":
                            msg = "ذخیره اطلاعات سوابق شغلی با خطا مواجه شد"
                            break;
                    }
                    break;
                default:
                    msg = "متاسفانه عملیات با خطا مواجه شد"
            }
            msg += "<br/>" +ErrorText+"<br/>"+ErrorPlace
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
    });
}
function HasAttr(item, attr)
{
    let a = $(item).attr(attr);
    return typeof attr !== 'undefined' && attr !== false;
}

function AddJsonItem(data, name, value)
{
    let json = {name: name, value: value}
    data.push(json)
    return data
}

$(".ErrorMessage a img").hover(
    function ()
    {
        let s = $(this).attr("src")
        s = s.replace("Return.png","Return-hover.png")
        $(this).attr("src",s)
    }
)
$(".ErrorMessage a img").mouseleave(
    function ()
    {
        let s = $(this).attr("src")
        s = s.replace("Return-hover.png","Return.png")
        $(this).attr("src",s)
    }
)
//*******************************Jobseeker**************************
function UpdateDetailTable(call_type, DetailType, data)
{   debugger;
    //chose detail table to edit
    let tbl = $("table."+DetailType)
    let IconPath = tbl.attr("IconPath")
    let id = data.DetailId
    //at first remove element row
    tbl.find("tr[data='"+id+"']").remove()

    // if it is add or update event, so we must add new row
    if (call_type != 'JobSeekerDetailDelete')
    {
        //create new row
        let new_row = "<tr class='"+DetailType+"' data='"+id+"'>"
        let row_content = ""
        //for each detail we have special columns, which their data is in data variable
        switch (DetailType)
        {
            case "EducationHistory":
                row_content = "<td>"+data.UniversityName+"</td>"
                row_content += "<td>"+data.EducationTendency+"</td>"
                row_content += "<td>"+data.DegreeTitle+"</td>"
                row_content += "<td>"
                row_content += '<form name="frmEducationHistory'+id+' class="EducationHistory">'
                row_content += '<input type="hidden" name="EducationHistoryId" value="'+id+'">'
                row_content += '<input type="hidden" name="UniversityProvince" value="'+data.UniversityProvince[0]+'">'
                row_content += '<input type="hidden" name="UniversityCity" value="'+data.UniversityCity[0]+'">'
                row_content += '<input type="hidden" name="UniversityType" value="'+data.UniversityType[0]+'">'
                row_content += '<input type="hidden" name="University" value="'+data.University[0]+'">'
                row_content += '<input type="hidden" name="UniversityDegree" value="'+data.UniversityDegree[0]+'">'
                row_content += '<input type="hidden" name="GPA" value="'+data.GPA[0]+'">'
                row_content += '<input type="hidden" name="FieldOfStudy" value="'+data.FieldOfStudy[0]+'">'
                row_content += '<input type="hidden" name="Tendency" value="'+data.Tendency[0]+'">'
                row_content += '<input type="hidden" name="StartYear" value="'+data.StartYear[0]+'">'
                row_content += '<input type="hidden" name="EndYear" value="'+data.EndYear[0]+'">'
                row_content += '<input type="hidden" name="JobSeeker" value="'+data.JobSeekerId[0]+'">'
                if (data.IsStudent != undefined)
                    row_content += '<input type="hidden" name="IsStudent" value="'+data.IsStudent[0]+'">'
                row_content += '</form>'
                break;
            case "JobHistory":
                row_content = "<td>"+data.CompanyTitle+"</td>"
                row_content += "<td>"+data.Role+"</td>"
                row_content += "<td>"+data.StartDateJalali+"</td>"
                row_content += "<td>"+data.EndDateJalali+"</td>"
                row_content += "<td>"
                row_content += '<form name="frmJobHistory'+id+' class="JobHistory">'
                row_content += '<input type="hidden" name="JobHistoryId" value="'+id+'">'
                row_content += '<input type="hidden" name="Company" value="'+data.Company[0]+'">'
                row_content += '<input type="hidden" name="Role" value="'+data.Role[0]+'">'
                row_content += '<input type="hidden" name="JobCategory" value="'+data.JobCategory[0]+'">'
                row_content += '<input type="hidden" name="StartDate" value="'+data.StartDateJalali+'">'
                row_content += '<input type="hidden" name="EndDate" value="'+data.EndDateJalali+'">'
                row_content += '<input type="hidden" name="IsWorking" '
                if (data.IsWorking != undefined)
                    row_content += 'value="' + data.IsWorking[0] + '"'
                row_content += '/>'
                row_content += '<input type="hidden" name="OrganizationUnit" value="'+data.OrganizationUnit[0]+'">'
                row_content += '<input type="hidden" name="Duties" value="'+data.Duties[0]+'">'
                row_content += '<input type="hidden" name="LeavingReason" value="'+data.LeavingReason[0]+'">'
                row_content += '<input type="hidden" name="Supervisor" value="'+data.Supervisor[0]+'">'
                row_content += '<input type="hidden" name="SupervisorRole" value="'+data.SupervisorRole[0]+'">'
                row_content += '<input type="hidden" name="JobLevel" value="'+data.JobLevel[0]+'">'
                row_content += '<input type="hidden" name="IsManager" '
                if (data.IsManager != undefined)
                    row_content += 'value="' + data.IsManager[0] + '"'
                row_content += '/>'
                row_content += '<input type="hidden" name="CoworkerCount" value="'+data.CoworkerCount[0]+'">'
                row_content += '</form>'
                break;
            case "PreferredCity":
                row_content = "<td>"+data.ProvinceTitle+"</td>"
                row_content += "<td>"+data.CityTitle+"</td>"
                row_content += "<td>"+data.PreferredCityPriority[0]+"</td>"
                row_content += "<td>"
                row_content += '<form name="frmJobHistory'+id+' class="PreferredCity">'
                row_content += '<input type="hidden" name="PreferredCityId" value="'+id+'">'
                row_content += '<input type="hidden" name="PreferredCityProvince" value="'+data.PreferredCityProvince[0]+'">'
                row_content += '<input type="hidden" name="PreferredCity" value="'+data.PreferredCity[0]+'">'
                row_content += '<input type="hidden" name="PreferredCityPriority" value="'+data.PreferredCityPriority[0]+'">'
                row_content += '</form>'
                break;
            case "PreferredJob":
                row_content = "<td>"+data.PreferredJobTitle+"</td>"
                row_content += "<td>"+data.PreferredJobPriority[0]+"</td>"
                row_content += "<td>"
                row_content += '<form name="frmPreferredJob'+id+' class="PreferredJob">'
                row_content += '<input type="hidden" name="PreferredJobId" value="'+id+'">'
                row_content += '<input type="hidden" name="PreferredJobPriority" value="'+data.PreferredJobPriority[0]+'">'
                row_content += '</form>'
                break
            case "JobSeekerSkill":
                row_content = "<td>"+data.SkillCategoryTitle+"</td>"
                row_content += "<td>"+data.SkillLevelTitle+"</td>"
                row_content += "<td>"+data.ExperienceMonth[0]+"</td>"
                row_content += "<td>"
                row_content += '<form name="frmJobSeekerSkill'+id+'" className="JobSeekerSkill">'
                row_content += '<input type="hidden" name="JobSeekerSkillId" value="'+id+'">'
                row_content += '<input type="hidden" name="SkillCategory" value="'+data.SkillCategory[0]+'">'
                row_content += '<input type="hidden" name="SkillLevel" value="'+data.SkillLevel[0]+'">'
                row_content += '<input type="hidden" name="ExperienceMonth" value="'+data.ExperienceMonth[0]+'">'
                row_content += '</form>'
                break
            case "Certification":
                row_content = "<td>"+data.CertificationTitle[0]+"</td>"
                row_content += "<td>"+data.InstituteTitle+"</td>"
                row_content += "<td>"+data.CertificationDate+"</td>"
                row_content += "<td>"
                row_content += '<form name="frmCertification'+id+'" className="Certification">'
                row_content += '<input type="hidden" name="CertificationlId" value="'+id+'">'
                row_content += '<input type="hidden" name="CertificationTitle" value="'+data.CertificationTitle[0]+'">'
                row_content += '<input type="hidden" name="CertificationGPA" value="'+data.CertificationGPA[0]+'">'
                row_content += '<input type="hidden" name="Institute" value="'+data.Institute[0]+'">'
                row_content += '<input type="hidden" name="CertificationDate" value="'+data.CertificationDate+'">'
                row_content += '</form>'
                break
            case "EmailAddress":
                row_content = "<td>"+data.EmailTitle[0]+"</td>"
                row_content += "<td>"+data.Email[0]+"</td>"
                row_content += "<td>"
                row_content += '<form name="frmEEmailAddress'+id+'" className="EmailAddress">'
                row_content += '<input type="hidden" name="EmailAddressId" value="'+id+'">'
                row_content += '<input type="hidden" name="Email" value="'+data.Email[0]+'">'
                row_content += '<input type="hidden" name="EmailTitle" value="'+data.EmailTitle[0]+'">'
                row_content += '</form>'
                break
            case "PhoneNumber":
                row_content = "<td>"+data.PhoneNumberTitle[0]+"</td>"
                row_content += "<td>"+data.TelType[0]+"</td>"
                row_content += "<td>"+data.TelNumber[0]+"</td>"
                row_content += "<td>"
                row_content += '<form name="frmPhoneNumber'+id+'" className="PhoneNumber">'
                row_content += '<input type="hidden" name="PhoneNumberId" value="'+id+'">'
                row_content += '<input type="hidden" name="PhoneNumberProvince" value="'+data.PhoneNumberProvince[0]+'">'
                row_content += '<input type="hidden" name="PhoneNumberCity" value="'+data.PhoneNumberCity[0]+'">'
                row_content += '<input type="hidden" name="TelType" value="'+data.TelType[0]+'">'
                row_content += '<input type="hidden" name="PhoneNumberTitle" value="'+data.PhoneNumberTitle[0]+'">'
                row_content += '<input type="hidden" name="TelNumber" value="'+data.TelNumber[0]+'">'
                row_content += '</form>'
                break
            case "PostalAddress":
                row_content = "<td>"+data.PostalAddressTitle[0]+"</td>"
                row_content += "<td>"+data.PostalAddressProvinceTitle+"</td>"
                row_content += "<td>"+data.PostalAddressCityTitle+"</td>"
                row_content += "<td>"+data.AddressText[0]+"</td>"
                row_content += "<td>"
                row_content += '<form name="frmPostalAddress'+id+'" className="PostalAddress">'
                row_content += '<input type="hidden" name="PostalAddressId" value="'+id+'">'
                row_content += '<input type="hidden" name="PostalAddressTitle" value="'+data.PostalAddressTitle[0]+'">'
                row_content += '<input type="hidden" name="PostalAddressProvince" value="'+data.PostalAddressProvince[0]+'">'
                row_content += '<input type="hidden" name="PostalAddressCity" value="'+data.PostalAddressCity[0]+'">'
                row_content += '<input type="hidden" name="PostalAddressCityDistrict" value="'+data.PostalAddressCityDistrict[0]+'">'
                row_content += '<input type="hidden" name="AddressText" value="'+data.AddressText[0]+'">'
                row_content += '<input type="hidden" name="PostalAddressNo" value="'+data.PostalAddressNo[0]+'">'
                row_content += '<input type="hidden" name="UnitNo" value="'+data.UnitNo[0]+'">'
                row_content += '<input type="hidden" name="PostalCode" value="'+data.PostalCode[0]+'">'
                row_content += '</form>'
            break

        }
        if (row_content != "")
        {
            row_content += "<img src='"+IconPath+"Edit.png' alt='ویرایش'" +
                " title='ویرایش' class='Edit Icon "+DetailType+"' data="+id+">"
            row_content +=  "<img src='"+IconPath+"Delete.png' alt='حذف'" +
                " title='حذف' class='Delete Icon "+DetailType+"' data="+id+">"
            row_content += "</td>"
            new_row += row_content + "</tr>"
            tbl.append(new_row)
            $(".JobSeeker .TableInfo."+DetailType+" tr[data='"+id+"'] .Edit.Icon").bind("click",
                function()
                {
                    TableInfoEdit(this)
                }
            )
            $(".JobSeeker .TableInfo."+DetailType+" tr[data='"+id+"'] .Delete.Icon").bind("click",
                function()
                {
                    TableInfoDelete(this)
                }
            )
        }
        //reset form to enter new data
        $("button."+DetailType+"[type='reset']").click()
        //empty detail id hidden input
        $("input[type='hidden'][name='"+DetailType+"Id']").val('')
        //hide all option of select for cascade combo
        //for example province and city combo
        //we select province p1 so all city of that province is shown
        //when we reset the form if we dont hide options, province would be empty
        //but city of province p1 is shown
        $("form[name='frm"+DetailType+"'] option").hide()
        //now show first element in combo
        $("form[name='frm"+DetailType+"'] option[value='0']").show()
        //now show parent combo element (exp: province)
        $("form[name='frm"+DetailType+"'] select.ParentCombo option").show()
    }

}
function ResizeWindow()
{
    let w = $( document ).width()
    if (w > 1500)
    {
        $(".JobSeekerPicture.Girl").show()
        $(".JobSeekerPicture.Boy").show()
    }
    else if (w < 1500 && w > 1000)
    {
        if ($("input.Gender:checked").val() == 1)
        {
            $(".JobSeekerPicture.Boy").show()
            $(".JobSeekerPicture.Girl").hide()
        }
        else
        {
            $(".JobSeekerPicture.Boy").hide()
            $(".JobSeekerPicture.Girl").show()
        }
    }
    else if (w < 1000)
    {
        $(".JobSeekerPicture.Girl").hide()
        $(".JobSeekerPicture.Boy").hide()
    }

}
$(".JobSeeker").ready(
    function () {
        ResizeWindow()
        $(".Searchable").select2()
        $(".Searchable").click(
            function()
            {
                $(window).scrollTop(0)
            }
        )
    }
)

function JobseekerValidator(RecordType)
{
    function NationalCodeValidator()
    {
        let N = $("#NationalCode")
        let code = N.val()
        let r = 0;
        if (!isNaN(code) && code != "") {

            let L = code.length;

            if (L < 8 || parseInt(code, 10) == 0) return -1;
            code = ('0000' + code).substr(L + 4 - 10);
            if (parseInt(code.substr(3, 6), 10) == 0)
            {
                N.parent("label").before("<p class='ErrorMessage'>کد ملی معتبر نیست</p>")
                return -2;
            }
            var c = parseInt(code.substr(9, 1), 10);
            var s = 0;
            for (var i = 0; i < 9; i++)
                s += parseInt(code.substr(i, 1), 10) * (10 - i);
            s = s % 11;
            if (!((s < 2 && c == s) || (s >= 2 && c == (11 - s))))
            {
                 N.parent("label").before("<p class='ErrorMessage'>کد ملی معتبر نیست</p>")
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
        function IsEmpty(value)
        {
            return value == '' || value == NaN || value == null || value == 0;
        }
        function RequiredField(Field)
        {
            let f =  $("form[name='frm"+RecordType+"'] [name='"+Field+"']")
            //date element is complex and contain 3 sub element day, month, year
            if (Field.endsWith("Date"))
            {
                if (IsEmpty(f.find(".Day").val()) || IsEmpty(f.find(".Month").val()) || IsEmpty(f.find(".Year").val()))
                {
                    f.addClass("RequiredError")
                    return -1;
                }
            }
            else if (IsEmpty(f.val()))
            {
                f.parent("label").addClass("RequiredError")
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
    function JobSeekerValidator()
    {
        let e = 0
        e += NationalCodeValidator()
        e += DateValidation("Birthdate")
        return e
    }
    function EducationHistoryValidator()
    {
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
    function DateValidation(date_class)
    {
        let e = 0
        let d = $("."+date_class+".Day").val()
        let m = $("."+date_class+".Month").val()
        let y = $("."+date_class+".Year").val()

        let d_not_empty = d != NaN && d != null && d != ""
        let m_not_empty = m != NaN && m != null && m != ""
        let y_not_empty = y != NaN && y != null && y != ""

        if ((d_not_empty && (!m_not_empty || !y_not_empty))
            || (m_not_empty && (!d_not_empty || !y_not_empty))
            || (y_not_empty && (!d_not_empty || !m_not_empty)))
        {
            ErrorMessage("."+date_class+".Day", "لطفا تاریخ را به صورت کامل وارد کنید")
            e=-1
        }
        return e
        /*let max_y = y.attr("max")
        let min_y = y.attr("min")
        if (y.val() > max_y || y.val() < min_y)
        {
            ErrorMessage(y,"سال را درست وارد کنید. بین \" + min_y + \" تا  \" + max_y" )
            r = -1
        }
        if (m.val() > 12 || m.val() < 1)
        {
            m.parent().before("<p class='ErrorMessage'> ماه را درست وارد کنید بین 1 تا 12</p>")
            m.addClass("ErrorBorder")
            r = -1
        }
        if ((d.val() > 31 && m.val() < 7)  || (d.val() > 30 && m.val() > 6)  || d.val() < 1)
        {
            d.parent().before("<p class='ErrorMessage'>روز را درست وارد کنید. بین 1 تا 31</p>")
            d.addClass("ErrorBorder")
            r = -1
        }
        return r*/
    }

    $(".Required").removeClass("RequiredError")
    $(".ErrorMessage").remove()
    $(".ErrorBorder").removeClass("ErrorBorder")
    let e = 0;

    let RequiredFields = []
    switch (RecordType)
    {
        case "JobSeeker":
            //set required fields
            RequiredFields = ["FirstName", "LastName"];
            e += JobSeekerValidator()
            break;
        case "EducationHistory":
            RequiredFields = ["Tendency", "UniversityDegree"]
            e +=  EducationHistoryValidator()
            break
        case "JobHistory":
            RequiredFields = ["Company", "Role", "StartDate"]
            break
        case "PreferredCity":
            RequiredFields = ["PreferredCity"]
            break;
        case "PreferredJob":
            RequiredFields = ["PreferredJob"]
            break;
        case "JobSeekerSkill":
            RequiredFields = ["SkillCategory"]
            break
        case "JobSeekerSkill":
            RequiredFields = ["SkillCategory"]
            break
        case "Certification":
            RequiredFields = ["CertificationTitle"]
            break
        case "PhoneNumber":
            RequiredFields = ["TelType","TelNumber"]
            break
        case "PostalAddress":
            RequiredFields = ["PostalAddressCity"]
            break
    }
    //check required fields
    e += RequiredFieldValidator(RequiredFields,RecordType)
    e += NumericValidator(RecordType)
    return e

}

function Save(SaveIcon)
{
    debugger
    let detail_type = $(SaveIcon).attr("data")
    let id = 0
    let crf_token = ""
    let data = {}
    let url = "/jobportal/jobseeker/save"
    let call_type = "JobSeekerSave"
    let e = 0
    e = JobseekerValidator(detail_type)
    let Form = $("form[name='frm"+detail_type+"']")

    //fill data of date field
    Form.find(".HiddenDate").each(
        function (index, item)
        {
            debugger
            name = $(item).attr("name")
            let d = Form.find("label[name='"+name+"']").find("Date.Day").val()
            let m = Form.find("label[name='"+name+"']").find("Date.Month").val()
            let y = Form.find("label[name='"+name+"']").find("Date.Year").val()
            if ($.isNumeric(d) && $.isNumeric(m) && $.isNumeric(y))
            {
                let date = y + '/' + m + '/' + d
                $(item).val(date)
            }
        }
    )

    // //fill other data
    // let SkillCategoryTitle = $("select[name='SkillCategory'] option:selected").text()
    // Form.find("input[name='SkillCategoryTitle']").val(SkillCategoryTitle)
    // let SkillLevelTitle = $("select[name='SkillLevel'] option:selected").text()
    // Form.find("input[name='SkillLevelTitle']").val(SkillLevelTitle)

    if (e >= 0)
    {
        //if select item is null, it would be deleted from serialization action
        //so we found all null value select item
        Form.find('select').each(
            function()
            {
                if ($(this).val() == null || $(this).val() == undefined)
                    $(this).val(0)
            }
        )
        data = Form.serializeArray();
        if (detail_type != "JobSeeker")
        {   debugger
            id = Form.find("input[name='"+detail_type+"Id']").val()
            //crf_token = $("input[name='csrfmiddlewaretoken']").val()
            //data = AddJsonItem(data, 'crf_token',crf_token)
            data = AddJsonItem(data, 'id',id)
            data = AddJsonItem(data, 'detail_type',detail_type)
            url = "/jobportal/jobseeker/detail/save"
            call_type = "JobSeekerDetailSave"
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
function TableInfoDelete(icon)
{
    let id = $(icon).attr("data")
    let detail_type = $(icon).parents('tr').attr("class")
    let crf_token = $("input[name='csrfmiddlewaretoken']").val()
    let data = {"id": id, "detail_type":detail_type, "csrfmiddlewaretoken":crf_token }
    RunAjax("/jobportal/jobseeker/detail/delete", "POST", data, "JobSeekerDetailDelete")
}
function FillDateInput(Date, DateLable)
{
    debugger;
    let d = Date.value.split('/')
    DateLable.find(".Day").val(d[2])
    DateLable.find(".Month").val(d[1])
    DateLable.find(".Year").val(d[0])
}

function TableInfoEdit(icon)
{
    debugger
    //let detail_frm = $(icon).parents(".Info").parent("div").children("form[name='frmEducationHistory']")
    let row_frm = $(icon).parent("td").children("form")
    let detail_type = $(icon).parents("tr").attr("class")
    //set detail id
    let id = $(icon).attr("data")
    $("input[type='hidden'][name='"+detail_type+"Id']").val(id)

    //get all data of this record
    let data = row_frm.serializeArray();
    let eleman = ""

    //chose detail form and fill with table info
    detail_frm = $("form[name='frm"+detail_type+"']")

    //for date variable, they are hidden element which contain full date
    detail_frm.find(".HiddenDate").each(
        function (index, elm)
        {
            eleman = elm
            $(data).each(
                function(index, d)
                {
                    let n = d.name
                    let v = d.value
                    e_name = $(eleman).attr("name")

                    if (e_name == n)
                    {
                         $(eleman).val(v)
                    }
                }
            )
        }
    )

    detail_frm.find("input").each(
        function (index, elm) {
            eleman = elm

            $(data).each(
                function (index, d)
                {
                    let n = d.name
                    let v = d.value
                    e_name = $(eleman).attr("name")

                    if (e_name == n)
                    {
                         $(eleman).val(v)
                    }
                }
            )
        }
    )
    detail_frm.find("select").each(
        function (index, elm) {
            eleman = elm
            $(data).each(
                function (index, d)
                {
                    let n = d.name
                    let v = d.value
                    let e_name = $(eleman).attr("name")
                    if (e_name == n)
                    {

                        $(eleman).val(v)
                        //in searchable combo must set text manually
                        if ($(eleman).hasClass('Searchable'))
                        {
                            $('#select2-'+e_name+'-container').text($('#'+e_name+' option:selected').text())
                        }

                    }
                }
            )
        }
    )
    detail_frm.find("input[type='checkbox']").each(
        function(index, elm){

            eleman = elm
            $(data).each(
                function(index,d)
                {

                    let n = d.name
                    let v = d.value
                    let e_name = $(eleman).attr("name")
                    if (e_name == n && v)
                    {
                    debugger
                        $(eleman).prop('checked', v);
                    }
                }
            )
        }
    )
     detail_frm.find("textarea").each(
        function (index, elm) {
            eleman = elm

            $(data).each(
                function (index, d)
                {
                    let n = d.name
                    let v = d.value
                    e_name = $(eleman).attr("name")

                    if (e_name == n)
                    {
                         $(eleman).val(v)
                    }
                }
            )
        }
     )
    //initiate date element (day, month, year)
    detail_frm.find(".DateInputs").each(
        function (index, elm) {
            eleman = elm
            let e_name = $(eleman).attr("name")
            $(data).each(
                function (index, d)
                {
                    let n = d.name
                    let v = d.value
                    if (e_name == n)
                    {
                        FillDateInput(d,$(eleman))
                    }
                }
            )
        }
    )
}

$(window).resize(function()
{
    ResizeWindow()
});

function ProvinceChange(Province, City)
{
    let p = Province.val()
    City.find("option").hide()
    City.find(".p"+p).show()
    City.val(0)
}
$(".JobSeeker #PreferredCityProvince").change(
    function ()
    {
        ProvinceChange($(this), $("#PreferredCity"))
    }
)
$(".JobSeeker #PostalAddressProvince").change(
    function ()
    {
        ProvinceChange($(this), $("#PostalAddressCity"))
    }
)
$(".JobSeeker #PostalAddressCity").change(
    function ()
    {
        let C = $(this).val()
        $("#PostalAddressCityDistrict").find("option").hide()
        $("#PostalAddressCityDistrict").find(".c"+C).show()
        $("#PostalAddressCityDistrict").val(0)
    }
)

$(".JobSeeker #PhoneNumberProvince").change(
    function()
    {
        ProvinceChange($(this), $("#PhoneNumberCity"))
    }
)
$(".JobSeeker #BirthProvince").change(
    function ()
    {
        ProvinceChange($(this), $("#BirthCity"))
    }
)
$(".JobSeeker #FieldOfStudy").change(
    function ()
    {
        f = this.value
        $("#Tendency option").hide()
        $("#Tendency .F_"+f).show()
        $("#Tendency").val(0)
    }
)

$(".JobSeeker #UniversityProvince").change(
    function ()
    {
        ProvinceChange($(this), $("#UniversityCity"))
        $("#UniversityType").val(0)
        $("#University").val(0)
        $("#UniversityType").change()
    }
)
$(".JobSeeker #UniversityCity").change(
    function ()
    {
        $("#UniversityType").val(0)
        $("#University").val(0)
        $("#UniversityType").change()
    }
)

$(".JobSeeker #UniversityType").change(
    function ()
    {
        $("#University").val(0)
        ut = this.value
        c = $("#UniversityCity").val()
        $("#University option").hide()
        if (c != NaN && c > 0 && ut != NaN && ut > 0)
        {
            $("#University .C_"+c+"_UT_"+ut).show()
        }
    }
)


$(".Gender").change(
    function ()
    {
        g = this.value
        if (g == Male)
        {
            ChangeImage($("#AvatarBoy"),"B-Gray.png","B-Shadow.png")
            ChangeImage($("#AvatarGirl"),"G-Shadow.png","G-Gray.png")
            $("#AvatarBoy").removeClass("opacity-50")
            $("#AvatarGirl").addClass("opacity-50")

        }
        else
        {
            ChangeImage($("#AvatarBoy"),"B-Shadow.png","B-Gray.png")
            ChangeImage($("#AvatarGirl"),"G-Gray.png","G-Shadow.png")
            $("#AvatarGirl").removeClass("opacity-50")
            $("#AvatarBoy").addClass("opacity-50")
        }
        ResizeWindow()
    }
)
$(".JobSeeker .Avatar").click(
    function ()
    {
        $("#AvatarFile").click()
    }
)
$(".JobSeeker .Avatar").hover(
    function ()
    {
        id = $(this).attr('id')
        if (id == 'AvatarGirl')
        {
             ChangeImage($(this),"G-Shadow.png","G-Normal.png")
        }
        else
        {
             ChangeImage($(this),"B-Shadow.png","B-Normal.png")
        }
    }
)
$(".JobSeeker .Avatar").mouseleave(
    function ()
    {
        id = $(this).attr('id')
        if (id == 'AvatarGirl')
        {
             ChangeImage($(this),"G-Normal.png","G-Shadow.png")
        }
        else
        {
             ChangeImage($(this),"B-Normal.png","B-Shadow.png")
        }
    }
)

$(".JobSeeker .RequiredError input").keypress(
    function ()
    {debugger
        let f = $(this)
        if (f.val() != '' && f.val() != NaN && f.val() != null)
            $(this).parent("label").removeClass("RequiredError")
    }
)

$(".JobSeeker .TableInfo .Delete.Icon").click(
    function ()
    {
        TableInfoDelete(this)
    }
)
$(".JobSeeker .TableInfo .Edit.Icon").click(
    function ()
    {
        TableInfoEdit(this)
    }
)
$(".JobSeeker .Title .TitleText").click(
    function ()
    {
        $(this).parent().next().slideToggle( "slow", function() {});
    }
)
$(".JobSeeker .Icon.Reset").click(
    function()
    {
        let ResetName = $(this).attr("data")
        $("button[type='reset']."+ResetName).click()
    })


$(".JobSeeker .Icon.Save").click(
    function()
    {
        Save(this)
    }
)