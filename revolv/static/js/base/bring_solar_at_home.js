
$(document).ready(function() {
     $(".grid-data").click(function(){
     var $this = $(this);
      var chapterUrl= 'chapter';
      window.location.href = chapterUrl;
 });
      $(".grid-data").mouseenter(function(){
        $(this).find(".data-text").css("color","#fff");
      });
    $(".grid-data").mouseleave(function(){
       $(this).find(".data-text").css("color","#666");
    });

    $(".get-start-btn").click(function(e){
        window.location.href = $(this).data('form-url');
    });
     $(".sign-up-revolve-update .form-checkbox").click(function(e){
         e.stopPropagation();
         console.log("clicked", $(this), $(this).find(".mark-checkbox"))
         var $this = $(this).find(".mark-checkbox");
         var checkboxSatus = $this.parent().data('checkbox-status');
         console.log(checkboxSatus)
         if(checkboxSatus == "checked") {
             $this.addClass('unmarked-checkbox');
             $this.removeClass('mark-checkbox');
             $this.parent().data('checkbox-status', "unchecked");
         } else {
             console.log("inside else")
                $this.addClass('mark-checkbox');
                $this.removeClass('unmarked-checkbox');
                $this.parent().data('checkbox-status', "checked");
         }
    });
});
var streamVideo = 0, element, instance;
function play(vidId) {
        instance = document.getElementById(vidId);
        instance.play();
        $(instance).next().css('display', 'none');
 }

function pause(vidId) {
        instance = document.getElementById(vidId);
            instance.pause();
            $(instance).next().css('display','flex');
}
 function showDesktopFullscreen(vidId) {
      element = document.getElementById(vidId);
  /*if (element.mozRequestFullScreen) {
    element.mozRequestFullScreen();
     element.play();
  } else if (element.webkitRequestFullScreen) {
    element.webkitRequestFullScreen();
    element.play();
  }*/
    $("#video-popup").show();
    instance.load();
    var popUpVideoId = document.getElementById("pop-up-video");
    console.log(popUpVideoId, $(element).find("source").attr('src'), $(element).attr('poster'))
    $(popUpVideoId).attr('poster', $(element).attr('poster'));
    $(popUpVideoId).find("source").attr('src', $(element).find("source").attr('src'));
    popUpVideoId.load();
    popUpVideoId.play();
  var vidNumber = parseInt($(element).attr('id').substr($(element).attr('id').length - 1));
    popUpVideoId.onended = function(e) {
	    (++vidNumber).toString();
	 	if(vidNumber < 6) {
	      	var nextVid = document.getElementById('video-'+ vidNumber);
	      	$(popUpVideoId).attr('poster', $(nextVid).attr('poster'));
		    $(popUpVideoId).find("source").attr('src', $(nextVid).find("source").attr('src'));
		    popUpVideoId.load();
		    popUpVideoId.play();
		}
    };
    $(".video-popup-body, #video-popup").click(function(e){
         e.stopPropagation();
         if (e.target !== this)
            return;
          $("#video-popup").hide();
    });
}
function goFullscreen(id) {
      element = document.getElementById(id);
 /* if (element.mozRequestFullScreen) {
    element.mozRequestFullScreen();
     element.play();
  } else if (element.webkitRequestFullScreen) {
    element.webkitRequestFullScreen();
    element.play();
  }*/
    $("#video-popup").show();

    var popUpVideoId = document.getElementById("pop-up-video");
    console.log(popUpVideoId, $(element).find("source").attr('src'), $(element).attr('poster'))
    $(popUpVideoId).attr('poster', $(element).attr('poster'));
    $(popUpVideoId).find("source").attr('src', $(element).find("source").attr('src'));
    popUpVideoId.load();
    popUpVideoId.play();
  var vidNumber = parseInt($(element).attr('id').substr($(element).attr('id').length - 1));
    popUpVideoId.onended = function(e) {
	    (++vidNumber).toString();
	 	if(vidNumber < 6) {
	      	var nextVid = document.getElementById('video-'+ vidNumber);
	      	$(popUpVideoId).attr('poster', $(nextVid).attr('poster'));
		    $(popUpVideoId).find("source").attr('src', $(nextVid).find("source").attr('src'));
		    popUpVideoId.load();
		    popUpVideoId.play();
		}
    };
 $(".video-popup-body, #video-popup").click(function(e){
         e.stopPropagation();
          if (e.target !== this)
            return;
          $("#video-popup").hide();
    });
}
$(document).keydown(function(e) {
    // ESCAPE key pressed
    if (e.keyCode == 27) {
         $("#video-popup").hide();
    }
});
/*$(document).on ('webkitfullscreenchange',function(){
      if(streamVideo == 0) {
      	streamVideo = 1;
      } else {
      	streamVideo = 0;
      	element.load();
      }
 });*/
/* $(".grid-data").on('click',function(){
 console.log("helllo");
      var $this = $(this);
      var chapterUrl= '/base/chapter.html'
      console.log($this.data('chapter-url'));
      window.location.href = chapterUrl;
 });*/

