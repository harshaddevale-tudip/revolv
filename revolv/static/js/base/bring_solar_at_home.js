document.getElementById('#desk-vid-1').onmouseout = function () {
   console.log("Hello")

}
var streamVideo = 0, element;
function playPause(vidId) {

	var instance = document.getElementById(vidId);
    if (instance.paused) {
        instance.play();
        $(instance).next().css('display', 'none');
    }
    else  {
        instance.pause();
        $(instance).next().css('display','flex');
 	}
}
 function showDesktopFullscreen(vidId) {
      element = document.getElementById(vidId);
  if (element.mozRequestFullScreen) {
    element.mozRequestFullScreen();
     element.play();
  } else if (element.webkitRequestFullScreen) {
    element.webkitRequestFullScreen();
    element.play();
  }
  var vidNumber = parseInt($(element).attr('id').substr($(element).attr('id').length - 1));
    element.onended = function(e) {
	    (++vidNumber).toString();
	 	if(vidNumber < 6) {
	      	var nextVid = document.getElementById('video-'+ vidNumber);
		    $(element).find("source").attr('src', $(nextVid).find("source").attr('src'));
		    element.load();
		    element.play();
		}
    };
}
function goFullscreen(id) {
      element = document.getElementById(id);
  if (element.mozRequestFullScreen) {
    element.mozRequestFullScreen();
     element.play();
  } else if (element.webkitRequestFullScreen) {
    element.webkitRequestFullScreen();
    element.play();
  }
    var vidNumber = parseInt($(element).attr('id').substr($(element).attr('id').length - 1));
    element.onended = function(e) {
	    (++vidNumber).toString();
	 	if(vidNumber < 6) {
	      	var nextVid = document.getElementById('video-'+ vidNumber);
		    $(element).find("source").attr('src', $(nextVid).find("source").attr('src'));
		    element.load();
		    element.play();
		}
    };
}
$(document).on ('webkitfullscreenchange',function(){
      if(streamVideo == 0) {
      	streamVideo = 1;
      } else {
      	streamVideo = 0;
      	element.load();
      }
 });