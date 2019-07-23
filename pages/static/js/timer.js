//To change what happens on timeout, edit function : countdownFinished() on line 91

var autotime = 10;

function autotimeout()
{
    if(autotime>0){
        $("#modalsubmit").text("OK (00:" + autotime + ")");
        autotime -= 1;
        setTimeout(function(){autotimeout()}, 1000);
    }else
        $("#frmsubmit").submit();
}

function autosubmit()
{
    $("#exampleModalCenter").click(function(e){$("#modalsubmit").click();})
    $("#exampleModalLongTitle").html("Time Up!<br>Test will now submit");
    $(".modalclose").attr("style", "display: none;");
    $("#btnsubmit").attr("style", "display: none;").click();
    $("#modalsubmit").text("OK");
    console.log("clicked");
    autotimeout();
}

$(document).ready(function(){
	TweenLite.defaultEase = Expo.easeOut;

    if(endtime - parseInt(timestamp()) > 0){
        var durmin = parseInt(endtime.substr(10,2)) - parseInt(timestamp().substr(10,2))
        var dursec = parseInt(endtime.substr(12,2)) - parseInt(timestamp().substr(12,2))
        if(dursec >= 60){
            durmin += 1;
            dursec -= 60;
        }
        if(dursec<0){
            durmin -= 1;
            dursec = (60+dursec)
        }
        if(durmin<0){
            durmin = (60+durmin)
        }
        dur = "" + ("00" + durmin).slice(-2) + ":" + ("00" + dursec).slice(-2);
        console.log(endtime + "\n" + timestamp() + "\n" + "\n" + dur)
    }else
        var dur = "00:01";
	initTimer(dur); // other ways --> "0:15" "03:5" "5:2"

	//var reloadBtn = document.querySelector('.reload');
	var timerEl = document.querySelector('.timer');

	function initTimer (t) {

	   var self = this,
		   timerEl = document.querySelector('.timer'),
		   minutesGroupEl = timerEl.querySelector('.minutes-group'),
		   secondsGroupEl = timerEl.querySelector('.seconds-group'),

		   minutesGroup = {
		      firstNum: minutesGroupEl.querySelector('.first'),
		      secondNum: minutesGroupEl.querySelector('.second')
		   },

		   secondsGroup = {
		      firstNum: secondsGroupEl.querySelector('.first'),
		      secondNum: secondsGroupEl.querySelector('.second')
		   };

	   var time = {
		  min: t.split(':')[0],
		  sec: t.split(':')[1]
	   };

	   var timeNumbers;

	   function updateTimer() {

		  var timestr;
		  var date = new Date();

		  date.setHours(0);
		  date.setMinutes(time.min);
		  date.setSeconds(time.sec);

		  var newDate = new Date(date.valueOf() - 1000);
		  var temp = newDate.toTimeString().split(" ");
		  var tempsplit = temp[0].split(':');

		  time.min = tempsplit[1];
		  time.sec = tempsplit[2];

		  timestr = time.min + time.sec;
		  timeNumbers = timestr.split('');
		  updateTimerDisplay(timeNumbers);


		  if(timestr === redtime){
		      $('.num').addClass("red");
		      $('.clock-separator').addClass("red");
		  }

		  if(timestr === '0000')
		     countdownFinished();

		  if(timestr != '0000')
		     setTimeout(updateTimer, 1000);

	   }

	   function updateTimerDisplay(arr) {

		  animateNum(minutesGroup.firstNum, arr[0]);
		  animateNum(minutesGroup.secondNum, arr[1]);
		  animateNum(secondsGroup.firstNum, arr[2]);
		  animateNum(secondsGroup.secondNum, arr[3]);

	   }

	   function animateNum (group, arrayValue) {

		  TweenMax.killTweensOf(group.querySelector('.number-grp-wrp'));
		  TweenMax.to(group.querySelector('.number-grp-wrp'), 1, {
		     y: - group.querySelector('.num-' + arrayValue).offsetTop
		  });

	   }

	   setTimeout(updateTimer, 870);

	}

	function countdownFinished() {
	    console.log(timestamp());
	    autosubmit();

	}
});
