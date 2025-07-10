//*******************************General**************************
function ChangeImage(img, old_name, new_name)
{
        s = img.attr("src")
        s = s.replace(old_name,new_name)
        img.attr("src",s)
}

function ChangeHoverImage(img, InOut)
{
    if (InOut == "I") //Mouse over
    {
        filepath = $(img).attr('src')
        //replace with hover image
        filepath = filepath.substring(0, filepath.length - 4)//remove .png
        filepath = filepath + '-hover.png'
        $(img).attr('src',filepath)
    }
    else // Mouse out
    {
        filepath = $(img).attr('src')
        //replace with hover image
        filepath = filepath.substring(0, filepath.length - 10)//remove -hover.png
        filepath = filepath + '.png'
        $(img).attr('src',filepath)

    }

}

function ViewCounter(QuestionId, CounterSpan, ParentCounter )
{

    v = CounterSpan.attr("data")
    v++
    CounterSpan.attr("data", v)
    CounterSpan.text("("+v+")")
    SaveCounter('QV', v, QuestionId)
    if (ParentCounter != null && !isNaN(ParentCounter))
    {
        v = ParentCounter.text().substring(1, (ParentCounter.text().length)-1)
        v++
        ParentCounter.attr("data", v)
        ParentCounter.text("("+v+")")
    }
}

function ShowHideAnswer(Answer, Arrow, qid, CounterSpan)
{
        if (Answer.hasClass("hide") && CounterSpan.html() !== '' )
            ViewCounter(qid, CounterSpan, null )

        Answer.toggleClass("hide")
        Arrow.toggleClass("arrow-left")
        Arrow.toggleClass("arrow-down")

}

function RunAjax(url, method, data)
{
    $.ajax({
        url : url, // the endpoint
        type : method, // http method
        data : data, // data sent with the get request

        // handle a successful response
        success : function(json) {
            console.log("success"); // another sanity check
        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    });
}

function KeywordSave(FAQ_id, Keyword, DeleteOrInsert)
{
    let url = "/FAQ/Confirm/keyword/"
    let method = "GET"
    let data = {
        FAQ_id: FAQ_id,
        Keyword: Keyword.trim(),
        DeleteOrInsert: DeleteOrInsert,
    }
    RunAjax(url, method, data)
}

function ConfirmFAQ(id, Question, Answer, ConfirmOrEdit)
{debugger
    let url = "/FAQ/Confirm/save/"
    let method = "GET"
    let data = {
        id: id,
        Question: Question,
        Answer: Answer,
        ConfirmOrEdit: ConfirmOrEdit
    }
    RunAjax(url, method, data)
}

function SaveCounter(CounterType, CounterValue, id){
    let url = "/FAQ/savecounter/"
    let method = "GET"
    let data = { CounterType : CounterType,
                CounterValue : CounterValue,
                id : id}
    RunAjax(url, method, data)
};


function SaveComment(Comment, id, FullName, Email, Corp ){
     let url = "/FAQ/savecomment/"
    let method = "GET"
    let data = { Comment : Comment,
                id : id,
                FullName: FullName,
                Email: Email,
                Corp: Corp}
    RunAjax(url, method, data)

};
///************************************FAG Page Begin*************************/
$(".accordion-label").click(
    function ()
    {
        input = $(this).parent().children("input")
        qid = input.attr("qid")
        if (input.prop('checked') == false ) {
            let CounterSpan =  $(this).find(" > .Question > * > * > .icon > .view")
            let ParentCounter = $(this).parents(".aspect-tab").find(".aspect-content .aspect-stat .ViewCount")
            ViewCounter(qid, CounterSpan, ParentCounter)

        }
        else
            input.prop('checked',false)
    }
)

$(".OperationIcon .like").click(
    function()
    {
        let likecount = $(this).attr("data");
        let qid = $(this).parents("p").attr("questionid");

        if (likecount == undefined || likecount == NaN)
            likecount = 0

        likecount++
        $(this).attr("data",likecount)
        $(this).parents(".QA").find("* > .icon > .like").text("("+likecount+")")
        $(this).parents(".QA").find("* > span.like").text("("+likecount+")")
        SaveCounter('QL', likecount, qid)
    })
$(".accordion-content .like").hover(
    function()
    {
        s = $(this).attr("src")
        s = s.replace("Like.png", "Like-hover.png")
        $(this).attr("src",s)
    })
$(".accordion-content .like").mouseleave(
    function()
    {
        s = $(this).attr("src")
        s = s.replace("Like-hover.png","Like.png")
        $(this).attr("src",s)
    })

$(".accordion-content .comment").hover(
    function()
    {
        s = $(this).attr("src")
        s = s.replace("Comment.png", "Comment-hover.png")
        $(this).attr("src",s)
    })
$(".accordion-content .comment").mouseleave(
    function()
    {
        s = $(this).attr("src")
        s = s.replace("Comment-hover.png","Comment.png")
        $(this).attr("src",s)
    })


$(".comment").click(
    function ()
    {
      $(this).parent().next().toggleClass("hide")
      //$(this).parent().next().find("textarea").focus()
    })
$(".comment-box .cancel").click(
    function ()
    {
         $(this).parents('.comment-box').addClass("hide")
    }
)
$(".comment-box .save").click(
    function ()
    {
        Comment = $(this).parents('.Comment-Form').find('* > * > [name="CommentText"]').val()
        id = $(this).attr("questionid")
        FullName = $(this).parents('.Comment-Form').find('* > * > [name="FullName"]').val()
        Email = $(this).parents('.Comment-Form').find('* > * > [name="Email"]').val()
        Corp = $(this).parents('.Comment-Form').find('* > * > [name="Corp"]').val()
        SaveComment(Comment, id, FullName, Email, Corp)
        $.alert({
        title: 'ذخیره موفقیت آمیز',
        content: "متن شما در سیستم ذخیره شد و پس از تایید مدیر سیستم نمایش داده خواهد شد",
        });

        $(".comment-box").hide()
    }
)
$(".FAQ .QA .row .Question").click(
    function()
    {
        Answer = $(this).parents(".QA").find(".Answer")
        CounterSpan = $(this).parents(".QA").find("* > span.view")
        qid = $(this).parents(".QA").find(".Question").attr("questionid")
        Arrow = $(this).parents(".QA").find("* > .arrow")

        ShowHideAnswer(Answer, Arrow, qid, CounterSpan)
    }
)

$(".FAQ .Menu li").click(
    function ()
    {
        if (!($(this).hasClass("Active")))
        {
            //remove class active from selected menu
            $(".FAQ .Menu li").removeClass("Active")
            //hide all projects QA
            $(".Project").addClass("hide")
            //active this menu
            $(this).addClass("Active")
            //get id of this project
            id = $(this).attr("project_id")
            //show this project QA
            $("#Project-" + id).removeClass("hide")
        }

    }
)
$(".FAQ").ready(
    function ()
    {
        let keyword = $(".Keywords i")
        $(".Keywords i").each(
        function (index, item)
        {
            $(item).html($(item).html().replace(/,/g, "</span><span>")+"</span>")
        })
    }
)

///************************************FAG Page End*************************/

//*******************************Search Result Start*****************************/
$(".SearchResult .row .Question").click(
    function()
    {
        Answer = $(this).next(".Answer")
        CounterSpan = $(this).find("* > span.view")
        qid = $(this).attr("questionid")
        Arrow = $(this).find("* > .arrow")

        ShowHideAnswer(Answer, Arrow, qid, CounterSpan)
    }
)
$(".SearchResult .ErrorMessage a img").hover(
    function ()
    {
        s = $(this).attr("src")
        s = s.replace("Return.png","Return-hover.png")
        $(this).attr("src",s)
    }
)
$(".SearchResult .ErrorMessage a img").mouseleave(
    function ()
    {
        s = $(this).attr("src")
        s = s.replace("Return-hover.png","Return.png")
        $(this).attr("src",s)
    }
)
$(".view-icon").click(
    function()
    {
        $(this).parents(".container").children("span").toggleClass("hide")
    }
)

//*******************************Search Result End*****************************/

///************************************Confirm Page Begin*************************/
/*$(".icon img").mouseover(
    function()
    {
        filepath = $(this).attr('src')
        //replace with hover image
        filepath = filepath.substring(0, filepath.length - 4)//remove .png
        filepath = filepath + '-hover.png'
        $(this).attr('src',filepath)
    }
)
$(".icon img").mouseout(
    function()
    {
        filepath = $(this).attr('src')
        //replace with hover image
        filepath = filepath.substring(0, filepath.length - 10)//remove -hover.png
        filepath = filepath + '.png'
        $(this).attr('src',filepath)
    }
)*/

$(".Confirm .icon img.confirm").click(
    function()
    {
        id = $(this).parent('.icon').attr("questionid")
        $.confirm({
            title: 'تایید پرسش و پاسخ',
            content: 'آیا از تایید این مورد اطمینان دارید؟',
            rtl: true,
            backgroundDismiss: true,
            autoClose: 'confirm|8000',
            buttons: {
                confirm:
                    {
                        btnClass:'btn-success',
                        text: 'تایید',
                        action:function () {
                            ConfirmFAQ(id,'','','C')
                            $.alert('مورد با موفقیت تایید شده و از این به بعد در لیست پرسش و پاسخ ها نمایش داده می شود');
                        }
                    },
                cancel:
                    {
                        btnClass:'btn-danger',
                        text: 'لغو',
                        action:function () {
                            $.alert('عملیات تایید لغو شد');
                        }
                    },
            }
        });
    }
)
function IconOperation(eleman)
{
    let Answer = eleman.parents(".QA").find(".Answer")
    let CounterSpan;
    let qid;
    let Arrow;

    if (Answer.hasClass("hide")) {
        CounterSpan = eleman.parents(".QA").find("* > span.view")
        qid = eleman.parents(".QA").find(".Question").attr("questionid")
        Arrow = eleman.parents(".QA").find("* > .arrow")
        ShowHideAnswer(Answer, Arrow, qid, CounterSpan)
    }

    eleman.parents('.row').children('.Question').find('.Edit').toggleClass("hide")
    eleman.parents('.row').children('.Question').find('.Label').toggleClass("hide")

    eleman.parents('.QA').find('.Answer > * > .Edit').toggleClass("hide")
    eleman.parents('.QA').find('.Answer > * > .Label').toggleClass("hide")

    eleman.parent().children('.edit').toggleClass("hide")
    eleman.parent().children('.save').toggleClass("hide")
    eleman.parent().children('.cancel').toggleClass("hide")
    eleman.parent().children('.confirm').toggleClass("hide")
}

$(".Confirm .icon img.cancel").click(
    function ()
    {
        IconOperation($(this))
    }
)
$(".Confirm .icon img.save").click(
    function ()
    {
        let QuestionText = $(this).parents('.row').children('.Question').find('.Edit input').val()
        QuestionText = QuestionText.trim().replace("\n","")
        let AnswerText = $(this).parents('.QA').find('.Answer > * > .Edit > textarea').val()
        AnswerText = AnswerText.trim().replace("\n","")
        let id = $(this).parent('.icon').attr("questionid")
        ConfirmFAQ(id, QuestionText, AnswerText, 'E')
        $.confirm({
            title: 'تایید به روزرسانی',
            content: 'اطلاعات جدید به روزرسانی شد. آیا مایل به تایید این مورد هستید؟',
            rtl: true,
            backgroundDismiss: true,
            autoClose: 'confirm|8000',
            buttons: {
                confirm:
                    {
                        btnClass:'btn-success',
                        text: 'تایید',
                        action:function () {
                            ConfirmFAQ(id,'','','C')
                            $.alert('مورد با موفقیت تایید شده و از این به بعد در لیست پرسش و پاسخ ها نمایش داده می شود');
                        }
                    },
                cancel:
                    {
                        btnClass:'btn-danger',
                        text: 'انصراف',
                        action:function () {
                            $.alert('عملیات تایید لغو شد');
                        }
                    },
            }
        });
        $(this).parents('.row').children('.Question').find('.Label').text(QuestionText)
        $(this).parents('.QA').find('.Answer > * > .Label').text(AnswerText)
        IconOperation($(this))
    }
)
$(".Confirm .icon img.edit").click(
    function ()
    {
        QuestionText =  $(this).parents('.row').children('.Question').find('.Edit').text()
        QuestionText = QuestionText.trim().replace("\n","")
        $(this).parents('.row').children('.Question').find('.Edit > .QuestionEdit').text(QuestionText)

        AnswerText =  $(this).parents('.QA').find('.Answer > * > .Edit > textarea').text()
        AnswerText = AnswerText.trim().replace("\n","")
        $(this).parents('.QA').find('.Answer > * > .Edit > textarea').text(AnswerText)

        IconOperation($(this))
    }
)
function KeywordIconOperation(element)
{
    element.parents(".Keywords").find(".NewKeyword").val("")
    element.parents(".Keywords").find(".NewKeyword").toggleClass("hide")
    element.parents(".Keywords").find(".add").toggleClass("hide")
    element.parents(".Keywords").find(".save").toggleClass("hide")
    element.parents(".Keywords").find(".cancel").toggleClass("hide")

}
$(".Confirm .Keywords .add").click(
    function () {
        KeywordIconOperation($(this))
    })

$(".Confirm .Keywords .save").click(
    function () {
        newkeyword = $(this).parents(".Keywords").find(".NewKeyword").val()
        id = $(this).parents(".Keywords").attr("questionid")
        KeywordSave(id, newkeyword, "I")
        src = $(".Keywords .Delete").attr('src')
        nkey = "<span>"+ newkeyword +"</span><img src='"+ src +"'  class='Delete' title='جهت حذف، کلیک نمایید'/>"
        $(this).parents(".Keywords").find(".NewKeyword").before(nkey)
        KeywordIconOperation($(this))
    })

$(".Confirm .Keywords .cancel").click(
    function () {
        KeywordIconOperation($(this))
    })

$(".Confirm .Menu li").click(
    function()
    {
        TeamCode = $(this).attr("data")
        $(".Inline.Photo img").addClass("hide")
        $(".Inline.Photo img." + TeamCode).removeClass("hide")
    }
)
$(".ErrorMessage .Login").mouseover(
    function ()
    {
        ChangeHoverImage(this, "I")
    }
)
$(".ErrorMessage .Login").mouseout(
    function ()
    {
        ChangeHoverImage(this, "O")
    }
)


///************************************Confirm Page End*************************/
