//var qid = "1";

function timestamp()
{
    var date = new Date();
    return "" + date.getFullYear() + ("0" + (date.getMonth()+1)).slice(-2) + ("0" + (date.getDate())).slice(-2) + ("0" + (date.getHours())).slice(-2) + ("0" + (date.getMinutes())).slice(-2) + ("0" + (date.getSeconds())).slice(-2);
}

function setCookie(ckey,cvalue,time) {
var d = new Date();
d.setTime(d.getTime() + (time*60*1000));
var expires = "expires=" + d.toGMTString();
document.cookie = ckey + "=" + cvalue + ";" + expires + ";path=/";
}

function savecook(opt)
{
  console.log(opt.attr("value"));
    setCookie(id_array[qid],opt.attr("value"), 30);
}

function delCookie(name) {
    document.cookie = name + '=;expires=Thu, 01 Jan 1970 00:00:01 GMT;path=/';
};

function getCookie(cname) {
var name = cname + "=";
var decodedCookie = decodeURIComponent(document.cookie);
var ca = decodedCookie.split(';');
for(var i = 0; i < ca.length; i++) {
var c = ca[i]; value="c"
while (c.charAt(0) == ' ') {
  c = c.substring(1);
}
if (c.indexOf(name) == 0) {
  return c.substring(name.length, c.length);
}
}
return "";
}

function setopt(abcd)
{
    if(abcd != "") {
        $("#" + abcd).addClass('clicked');
        $("#" + abcd).parent().parent().parent().addClass('glow');
        $("#" + abcd).find('p').addClass('hide');
    }
    if(abcd!="a"){
      $("#a").removeClass('clicked');
      $("#a > p").removeClass('hide');
      $("#a").parent().parent().parent().removeClass('glow');
    }
    if(abcd!='b'){
      $('#b').removeClass('clicked');
     $("#b > p").removeClass("hide");
     $("#b").parent().parent().parent().removeClass('glow');
   }
    if(abcd!='c'){
      $('#c').removeClass('clicked');
     $("#c > p").removeClass("hide");
     $("#c").parent().parent().parent().removeClass('glow');
   }
    if(abcd!='d'){
      $('#d').removeClass('clicked');
     $("#d > p").removeClass("hide");
     $("#d").parent().parent().parent().removeClass('glow');
   }
}


function getQuestion(reqQid)
{
    $("#quedisp").addClass("hide");
    $(".opt-container").addClass("hide");
    $.ajax({
        headers: { "X-CSRFToken": csrf },
        data:{reqid: reqQid, time: timestamp()},
        url: "api/",
        method: "POST",
        success: function (res) {
        if(res.err == null)
        {
            setTimeout(function(){
                qid=reqQid;
                $("#quedisp").html(res.que);
                $("#qnum").text("Question No. " + qid);
                $("#a").parent().parent().parent().find('.opttxt').text(res.opt1);
                $("#b").parent().parent().parent().find('.opttxt').text(res.opt2);
                $("#c").parent().parent().parent().find('.opttxt').text(res.opt3);
                $("#d").parent().parent().parent().find('.opttxt').text(res.opt4);
                setopt(getCookie(id_array[qid]));
                $("#quedisp").removeClass("hide");
                $(".opt-container").removeClass("hide");
                if(qid == 1)
                    $("#btnprev").attr("disabled", true);
                else
                    $("#btnprev").attr("disabled", false);
                if(qid == id_array.length-1)
                    $("#btnnext").attr("disabled", true);
                else
                    $("#btnnext").attr("disabled", false);
            }, 200);
        }else if(res.err = "errdt")
            alert("Date and Time error!\nPlease contact Pulzion '19 volunteer.");
        }
    });
}

getQuestion(1);

function bookmark()
{
    if($("#q"+qid).find('.fa').hasClass('hide'))
        $("#q"+qid).find('.fa').removeClass('hide')
    else
        $("#q"+qid).find('.fa').addClass('hide')
}

//  $('.op1').click(function(){
//    //console.log("ok");
//
//    $(this).find('.left').find('.c2').click();
//  });

  $('.op1').click(function () {
    if($(this).find('.left').find('.c2').hasClass('clicked')){
      $(this).find('.left').find('.c2').removeClass('clicked');
      $(this).find('.left').find('.c2').find('p').removeClass('hide');
      delCookie(id_array[qid]);
      $(this).find('.left').find('.c2').parent().parent().parent().removeClass('glow');
      $("#q"+qid).removeClass('book');
    }
    else
    {
      $("#q"+qid).addClass('book');
      $(this).find('.left').find('.c2').addClass('clicked');
      $(this).find('.left').find('.c2').parent().parent().parent().addClass('glow');
      savecook($(this).find('.left').find('.c2').parent().parent().parent());
      $(this).find('.left').find('.c2').find('p').addClass('hide');
    //$("#pa").addClass('hide');



    if($(this).find('.left').find('.c2').attr("id")!="a"){
      $("#a").removeClass('clicked');
      $("#a > p").removeClass('hide');
      $("#a").parent().parent().parent().removeClass('glow');
    }
    if($(this).find('.left').find('.c2').attr("id")!='b'){
      $('#b').removeClass('clicked');
     $("#b > p").removeClass("hide");
     $("#b").parent().parent().parent().removeClass('glow');
   }
    if($(this).find('.left').find('.c2').attr("id")!='c'){
      $('#c').removeClass('clicked');
     $("#c > p").removeClass("hide");
     $("#c").parent().parent().parent().removeClass('glow');
   }
    if($(this).find('.left').find('.c2').attr("id")!='d'){
      $('#d').removeClass('clicked');
     $("#d > p").removeClass("hide");
     $("#d").parent().parent().parent().removeClass('glow');
   }
  }

});


function sub()
{
    var obj = {};
    var cookie = document.cookie.split(";");
    // $("#modalsubmit").attr("disabled", true).text("Submitting test...");
    // document.getElementById("modalsubmit").disabled = true;
    // document.getElementById("modalsubmit").innerText = "Submitting test...";
    for (x in cookie){
        if(x>0&&(cookie[x].split(":")[0].split(" ")[1].split("=")[0]!='csrftoken'))
        {
            obj[cookie[x].split(":")[0].split(" ")[1].split("=")[0]] = cookie[x].split("=")[1];
            console.log(cookie[x].split("=")[1].split(";")[1]);

        }

    }
    document.getElementById("inpans").value = JSON.stringify(obj);
    document.getElementById("modalsubmit").value = "Submitting test...";
    document.getElementById("modalsubmit").disabled = true;
    console.log("\n\n" + JSON.stringify(obj));
    // deleteAllCookies();

    return true;
}