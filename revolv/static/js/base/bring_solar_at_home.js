
$(document).ready(function() {
     $(".grid-data").click(function(){
     var $this = $(this);
      var chapterUrl= 'chapter';
      console.log($this.data('chapter-url'));
      window.location.href = chapterUrl;
 });

});
var streamVideo = 0, element;
function play(vidId) {
	var instance = document.getElementById(vidId);
        instance.play();
        $(instance).next().css('display', 'none');
 }
function pause(vidId) {
	var instance = document.getElementById(vidId);
        instance.pause();
        $(instance).next().css('display','flex');
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
/* $(".grid-data").on('click',function(){
 console.log("helllo");
      var $this = $(this);
      var chapterUrl= '/base/chapter.html'
      console.log($this.data('chapter-url'));
      window.location.href = chapterUrl;
 });*/
