

$(".SystemInfo").closest(".parent-div-item").addClass("Hide")
$(".SystemInfo.Level-0").closest(".parent-div-item").removeClass("Hide")


/*$(".img-profile").each(function(){
    var img = $(this);
    var src = (img.attr("gender") == "m") ? img.attr("default-src-m") : img.attr("default-src-f");
    if(img[0].naturalWidth ==0 ) {
        img.attr("src",src);
    }
});*/

$('.SystemInfo').click(function () {
        if (!$(this).hasClass('HasURL')) {
            var id = $(this).attr('id')
            id =id.substring(11)
            //$('.SystemInfo').addClass('Hide')
            $(".SystemInfo").closest(".parent-div-item").addClass("Hide")
            //$('.SystemInfo.Parent-'+id).removeClass('Hide')
            $('.SystemInfo.Parent-'+id).closest(".parent-div-item").removeClass("Hide")
        }
    });



$('.up-btn').click(function () {
        var level;
        var Parent=$(".parent-div-item").not('.Hide').find(".SystemInfo").attr('class')
        var parentid=$(".parent-div-item").not('.Hide').find(".SystemInfo").attr('parentid')
        var ParentClass = Parent.split(' ')
        ParentClass.forEach(function(value, index) {
             if (value.indexOf('Level')>=0) {
                 level=value.split('-')[1]
             }
        });
        if (parseInt(level)>0){
           level=parseInt(level)-1;

           //$('.SystemInfo').addClass('Hide')
            $(".SystemInfo").closest(".parent-div-item").addClass("Hide")

            $('.SystemInfo.Level-'+level.toString()).each(function (){

               if($(this).attr('id')=='SystemInfo-'+parentid){
                   //$(this).removeClass('Hide')
                   $(this).closest(".parent-div-item").removeClass("Hide")
               }
           })

        }

        if(parseInt(level)==0){
            //$('.Parent-None').removeClass('Hide')
            $(".SystemInfo").closest(".parent-div-item").addClass("Hide")
            $('.Parent-None').closest(".parent-div-item").removeClass("Hide")
        }

    });

function ChangeImage(img, old_name, new_name)
{
        var s = img.attr("src")
        s = s.replace(old_name,new_name)
        img.attr("src",s)
}

function ChangeHoverImage(img, InOut)
{
    if (InOut == "I") //Mouse over
    {
        var filepath = $(img).attr('src')
        //replace with hover image
        filepath = filepath.substring(0, filepath.length - 4)//remove .png
        filepath = filepath + '-hover.svg'
        $(img).attr('src',filepath)
    }
    else // Mouse out
    {
        filepath = $(img).attr('src')
        //replace with hover image
        filepath = filepath.substring(0, filepath.length - 10)//remove -hover.png
        filepath = filepath + '.svg'
        $(img).attr('src',filepath)

    }

}

$(".Menu-Icon").click(
    function ( )
    {
          $('.Menu-Icon').not('.Icon-hover').each(
              function (index, item)
              {
                  filepath = $(item).attr('src')
                  filepath = filepath.substring(0, filepath.length - 10) //remove .png
                  filepath = filepath + '.svg'
                  $(item).attr('src',filepath)
              }
          )
          $('.Menu-Icon').not('.Icon-hover').addClass('Icon-hover')



        if ($(this).hasClass('Icon-hover'))
        {
          filepath = $(this).attr('src')
            //replace with hover image
          filepath = filepath.substring(0, filepath.length - 4) //remove .png
          filepath = filepath + '-hover.svg'

          $(this).attr('src',filepath)
          $(this).removeClass('Icon-hover')
        }
    }
)

$(".select-user-for-translate").select2();
// function ChangeImage(img, old_name, new_name)
// {
//     let s = img.attr("src")
//     s = s.replace(old_name,new_name)
//     img.attr("src",s)
// }
//
//
// $('.Gender').change(
//     function ()
//
//     {
//         // alert('Hello2')
//         // debugger
//         g = this.value
//         if (g == 'Male')
//         {
//             ChangeImage($("#AvatarBoy"),"B-Gray.png","B-Normal.png")
//             ChangeImage($("#AvatarGirl"),"G-Normal.png","G-Gray.png")
//             $("#AvatarBoy").removeClass("opacity-50")
//             $("#AvatarGirl").addClass("opacity-50")
//
//         }
//         else
//         {
//             ChangeImage($("#AvatarBoy"),"B-Normal.png","B-Gray.png")
//             ChangeImage($("#AvatarGirl"),"G-Gray.png","G-Normal.png")
//             $("#AvatarGirl").removeClass("opacity-50")
//             $("#AvatarBoy").addClass("opacity-50")
//         }
//         ResizeWindow()
//     }
// )
// $(".Avatar").click(
//     function ()
//     {
//         $("#AvatarFile").click()
//     }
// )
// $(".Avatar").hover(
//     function ()
//     {
//         id = $(this).attr('id')
//         if (id == 'AvatarGirl')
//         {
//              ChangeImage($(this),"G-Shadow.png","G-Normal.png")
//         }
//         else
//         {
//              ChangeImage($(this),"B-Shadow.png","B-Normal.png")
//         }
//     }
// )
// $(".Avatar").mouseleave(
//     function ()
//     {
//         id = $(this).attr('id')
//         if (id == 'AvatarGirl')
//         {
//              ChangeImage($(this),"G-Normal.png","G-Shadow.png")
//         }
//         else
//         {
//              ChangeImage($(this),"B-Normal.png","B-Shadow.png")
//         }
//     }
// )
//
// $(".pdatepicker").persianDatepicker({
//             format: 'YYYY/MM/DD',
//
//  });
//
// function ProvinceChange(Province, City)
// {
//     let p = Province.val()
//     City.find("option")Hide()
//     City.find(".p"+p).show()
//     City.val(0)
// }
//
// $("#TelProvince").change(
//     function ()
//     {
//         ProvinceChange($(this), $("#TelCity"))
//     }
// )
//
// $("#UniProvince").change(
//     function ()
//     {
//         ProvinceChange($(this), $("#UniCity"))
//     }
// )
// $("#AddressProvince").change(
//     function ()
//     {
//         ProvinceChange($(this), $("#AddressCity"))
//     }
// )
// $('.Title').click(
//     function ()
//     {
//         $(this).next('.body').slideToggle();
//     }
// )
//
// $("#UniProvince").change(
//     function ()
//     {
//         ProvinceChange($(this), $("#UniCity"))
//     }
// )
//
// $("#UniversityType").change(
//     function ()
//     {
//         $("#Uni").val(0)
//         ut = this.value
//         c = $("#UniCity").val()
//         $("#Uni option")Hide()
//         if (c != NaN && c > 0 && ut != NaN && ut > 0)
//         {
//             $("#Uni .C_"+c+"_UT_"+ut).show()
//         }
//
//     }
// )
//
// $("#UniProvince").change(
//     function ()
//     {
//         ProvinceChange($(this), $("#UniCity"))
//         $("#UniversityType").val(0)
//         $("#University").val(0)
//         $("#UniversityType").change()
//     }
// )
// $("#UniCity").change(
//     function ()
//     {
//         $("#UniversityType").val(0)
//         $("#Uni").val(0)
//         $("#UniversityType").change()
//     }
// )
//
// //
// // function PeronValidator(RecordType)
// // {
// //     function NationalCodeValidator()
// //     {
// //         let N = $("#NationalCode")
// //         let code = N.val()
// //         let r = 0;
// //         if (!isNaN(code) && code != "") {
// //
// //             let L = code.length;
// //
// //             if (L < 8 || parseInt(code, 10) == 0) return -1;
// //             code = ('0000' + code).substr(L + 4 - 10);
// //             if (parseInt(code.substr(3, 6), 10) == 0)
// //             {
// //                 N.parent("label").before("<p class='ErrorMessage'>کد ملی معتبر نیست</p>")
// //                 return -2;
// //             }
// //             var c = parseInt(code.substr(9, 1), 10);
// //             var s = 0;
// //             for (var i = 0; i < 9; i++)
// //                 s += parseInt(code.substr(i, 1), 10) * (10 - i);
// //             s = s % 11;
// //             if (!((s < 2 && c == s) || (s >= 2 && c == (11 - s))))
// //             {
// //                  N.parent("label").before("<p class='ErrorMessage'>کد ملی معتبر نیست</p>")
// //                 return  -3;
// //             }
// //         }
// //         return r
// //     }
// //     function ErrorMessage(element, msg)
// //     {
// //         $(element).parent().before("<p class='ErrorMessage'>"+msg+"</p>")
// //         $(element).addClass("ErrorBorder")
// //     }
// //     function RequiredFieldValidator(Fields, RecordType)
// //     {
// //         function IsEmpty(value)
// //         {
// //             return value == '' || value == NaN || value == null || value == 0;
// //         }
// //         function RequiredField(Field)
// //         {
// //             let f =  $("form[name='frm"+RecordType+"'] [name='"+Field+"']")
// //             //date element is complex and contain 3 sub element day, month, year
// //             if (Field.endsWith("Date"))
// //             {
// //                 if (IsEmpty(f.find(".Day").val()) || IsEmpty(f.find(".Month").val()) || IsEmpty(f.find(".Year").val()))
// //                 {
// //                     f.addClass("RequiredError")
// //                     return -1;
// //                 }
// //             }
// //             else if (IsEmpty(f.val()))
// //             {
// //                 f.parent("label").addClass("RequiredError")
// //                 return -1;
// //             }
// //             return 0;
// //         }
// //         let e = 0;
// //         $.each(Fields,
// //             function (index, value)
// //             {
// //                 e = RequiredField(value)
// //             })
// //         return e
// //     }
// //     function  PeronValidator()
// //     {
// //         let e = 0
// //         e += NationalCodeValidator()
// //         e += DateValidation("Birthdate")
// //         return e
// //     }
// //     function EducationHistoryValidator()
// //     {
// //         return 0
// //     }
// //     function NumericValidator(RecordType)
// //     {
// //         let e = 0
// //         //check all numeric input with min/max value
// //         $("form[name='frm"+RecordType+ "']").find("input[type='number']").each(
// //             function(index, item)
// //             {
// //                 //if item has value, check it
// //                 if ($(item).val() != NaN && $(item).val() != null)
// //                 {
// //                     if (HasAttr(item,"min") && parseInt($(item).attr("min")) > parseInt($(item).val()))
// //                     {
// //                         ErrorMessage(item, "مقدار بایستی بیشتر از "  + $(item).attr("min") + " باشد.")
// //                         e += -1
// //                     }
// //                     if (HasAttr(item,"max") && parseInt($(item).attr("max")) < parseInt($(item).val()))
// //                     {
// //                         ErrorMessage(item, "مقدار بایستی کمتر از "  + $(item).attr("max") + " باشد.")
// //                         e += -1
// //                     }
// //
// //                 }
// //
// //             }
// //         )
// //         return e
// //     }
// //     function DateValidation(date_class)
// //     {
// //         let e = 0
// //         let d = $("."+date_class+".Day").val()
// //         let m = $("."+date_class+".Month").val()
// //         let y = $("."+date_class+".Year").val()
// //
// //         let d_not_empty = d != NaN && d != null && d != ""
// //         let m_not_empty = m != NaN && m != null && m != ""
// //         let y_not_empty = y != NaN && y != null && y != ""
// //
// //         if ((d_not_empty && (!m_not_empty || !y_not_empty))
// //             || (m_not_empty && (!d_not_empty || !y_not_empty))
// //             || (y_not_empty && (!d_not_empty || !m_not_empty)))
// //         {
// //             ErrorMessage("."+date_class+".Day", "لطفا تاریخ را به صورت کامل وارد کنید")
// //             e=-1
// //         }
// //         return e
// //         /*let max_y = y.attr("max")
// //         let min_y = y.attr("min")
// //         if (y.val() > max_y || y.val() < min_y)
// //         {
// //             ErrorMessage(y,"سال را درست وارد کنید. بین \" + min_y + \" تا  \" + max_y" )
// //             r = -1
// //         }
// //         if (m.val() > 12 || m.val() < 1)
// //         {
// //             m.parent().before("<p class='ErrorMessage'> ماه را درست وارد کنید بین 1 تا 12</p>")
// //             m.addClass("ErrorBorder")
// //             r = -1
// //         }
// //         if ((d.val() > 31 && m.val() < 7)  || (d.val() > 30 && m.val() > 6)  || d.val() < 1)
// //         {
// //             d.parent().before("<p class='ErrorMessage'>روز را درست وارد کنید. بین 1 تا 31</p>")
// //             d.addClass("ErrorBorder")
// //             r = -1
// //         }
// //         return r*/
// //     }
// //
// //     $(".Required").removeClass("RequiredError")
// //     $(".ErrorMessage").remove()
// //     $(".ErrorBorder").removeClass("ErrorBorder")
// //     let e = 0;
// //
// //     let RequiredFields = []
// //     switch (RecordType)
// //     {
// //         case " Peron":
// //             //set required fields
// //             RequiredFields = ["FirstName", "LastName"];
// //             e +=  PeronValidator()
// //             break;
// //         case "EducationHistory":
// //             RequiredFields = ["Tendency", "UniversityDegree"]
// //             e +=  EducationHistoryValidator()
// //             break
// //         case " PeronHistory":
// //             RequiredFields = ["Company", "Role", "StartDate"]
// //             break
// //         case "PreferredCity":
// //             RequiredFields = ["PreferredCity"]
// //             break;
// //         case "PreferredJob":
// //             RequiredFields = ["PreferredJob"]
// //             break;
// //         // case "JobSeekerSkill":
// //         //     RequiredFields = ["SkillCategory"]
// //         //     break
// //         // case "JobSeekerSkill":
// //         //     RequiredFields = ["SkillCategory"]
// //         //     break
// //         case "Certification":
// //             RequiredFields = ["CertificationTitle"]
// //             break
// //         case "PhoneNumber":
// //             RequiredFields = ["TelType","TelNumber"]
// //             break
// //         case "PostalAddress":
// //             RequiredFields = ["PostalAddressCity"]
// //             break
// //     }
// //     //check required fields
// //     e += RequiredFieldValidator(RequiredFields,RecordType)
// //     e += NumericValidator(RecordType)
// //     return e
// //
// // }