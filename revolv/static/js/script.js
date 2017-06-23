$(document).ready(function(){
    $('#dropdown-select-text').on('click', function() {
    $('.dropdown-menu').toggle();
    });
    $('.option').on('click', function() {
        $(this).closest('.dropdown-menu').hide();
        $(this).parents('.dropdown').find('.dropdown-title span:first-child').text($(this).html());
        $(this).parents('.dropdown').find('.dropdown-select').val($(this).html());
        selectedValue=$(this).data("selected-state");
        changeFunc(selectedValue);
    });

     function changeFunc(selectedValue) {


       var states1 = ["AZ","CO","CT","DC","DE","FL", "GA","IL","IN","LA","MD","ME", "MI","MN","MO","NC","NH","NM","NV","OH","PA","RI","TX", "UT","VA","VT","WI"];
       var states2 = ["AK","AL", "AR","CA", "HI","IA", "ID", "KS","KY", "MA","MS", "MT","ND", "NE", "NJ","NY",
                      "OK", "OR", "SC","TN", "WA", "WV","WY"];

        for (i=0;i<50;i++)
        {
            if (selectedValue == states1[i])
            {
                $("#img").attr("src",'/static/images/EnergySage_updated.jpg');
                $("#invstr-logo-link").attr("href",'http://www.energysage.com/p/re-volv/');
                $("#invstr-logo-link").attr("target",'_blank');
                $(".investor-remaining-img").hide();
                $(".selected-logo").css('border','0');
                $("#img").closest(".invstr-logo-images").removeClass("col-sm-4");
                $("#img").closest(".invstr-logo-images").addClass("col-sm-6");
                $(".investors_logo_text").text("The easiest way to go solar! Installers compete for your business to give you more options and the best deal. Free instant solar estimate.");
            }
            else if (selectedValue == states2[i])
            {
                $("#img").attr("src","/static/images/PickMySolar_updated.png");
                $("#invstr-logo-link").attr("href",'http://info.pickmysolar.com/re-volv-partner/');
                $("#invstr-logo-link").attr("target",'_blank');
                $(".investor-remaining-img").hide();
                $(".selected-logo").css('border','0');
                $("#img").closest(".invstr-logo-images").removeClass("col-sm-4");
                $("#img").closest(".invstr-logo-images").addClass("col-sm-6");
                $(".investors_logo_text").text("Go solar hassle-free with Pick My Solar. Easily compare solar companies to get the best deal on your solar project. When solar companies compete, you win!");
            }

        }
   }
    $(document).click(function (event) {
        var clickover = $(event.target);
        var _opened = $(".navbar-collapse").hasClass("collapse in");
        if (_opened === true ) {
            $("button.navbar-toggle").click();
        }
    });
    $(document).mouseup(function (e) {
         var popup = $(".dropdown-menu");
         if (!$('#dropdown-select-text').is(e.target) && !$('#dropdown-title').is(e.target) && !$('#dropdown-title span').is(e.target) &&
             !popup.is(e.target) && popup.has(e.target).length == 0) {
             popup.hide();
             $('.dropdown-triangle').html('▾');
         }
     });
    $('#dropdown-select-text, .option').on('click', function() {
    if ($('.dropdown-triangle').html() == '▾') {
        $('.dropdown-triangle').html('▴');
    }
    else if ($('.dropdown-triangle').html() == '▴'){
        $('.dropdown-triangle').html('▾');
    }
    });

    $(document).on('click', '#stOverlay', function(e) {
        window.location.href='/my-portfolio/';
    });
     $(document).on('click', '#share-modal', function(e) {
        if(e.target!== this)
        return;
        window.location.href='/my-portfolio/';
    });
      $(document).on('click', '#share-signup-modal', function(e) {
        if(e.target!== this)
        return;
        window.location.href='/my-portfolio/';
    });

     $(".stripe-button-el").click(function(){
         if($(this).find("span:last-child").text() != "Next") {
            $(".input-custom-amount input[type=number]").val($(this).find("span:last-child").text());
         }
     });
    // $(".u-background--grey div:first-child").off();
     $(".u-background--grey label").click(function() {
       console.log("clicked")
          $(".monthly-plan-msg").toggle();
     });
     $(".input-custom-amount input[type=number]").change(function(){
       if($(this).val().trim() > 0) {
           $(".donate-popup .next-button").addClass("stripe-button-el");
           $(".donate-popup .next-button").css("background-color", "#4EB181");
           $(".donate-popup .next-button").removeClass("disable-donation-btn");
       } else {
          $(".donate-popup .next-button").css("background-color", "#9a9a9a");
           $(".donate-popup .next-button").removeClass("stripe-button-el");
           $(".donate-popup .next-button").addClass("disable-donation-btn");
       }
     });
     $(document).on('click','.stripe-button-el',function (e) {
          $(this).closest(".modal").hide();
     });
      $(document).click(function (event) {
          var clickover = $(event.target);
          var _opened = $(".navbar-collapse").hasClass("collapse in");
          if (_opened === true ) {
              $('.navbar-collapse').collapse('hide');
            }
          });
            $(".navbar-toggle").click(function (event) {
          var clickover = $(event.target);
          var _opened = $(".navbar-collapse").hasClass("collapse in");
          if (_opened === true ) {
          	  $('.navbar-collapse').removeClass('in');
			  event.stopPropagation();
            }
          });
          $(".right-list").click(function() {
              window.location.href = $(this).data('chapter-url');

          });


  //click Down arrow in Home page
  $(".down-arrow-button").click(function(){
    var scroll_offset = $(".active-projects-module").offset();
    $("body,html").animate({
      scrollTop:scroll_offset.top
    },1000);
    setTimeout(function(){
      if(!$("header").hasClass("after-scroll-header"))
      {
        $("header").removeClass("top-section-header").addClass("after-scroll-header");
        $("header").hide();
        $("header").slideDown();
      }
    },1500)

  });

  //click option in Dropdown list
  $(".dropdown-menu li a").click(function(){
    $(this).parents(".dropdown").find("li a").removeClass("active");
    $(this).addClass("active");

    $(this).parents(".dropdown").find(".selected-option").html($(this).html());
    $(this).parents(".dropdown").find(".selected-option").attr("title",$(this).html());
  });

  //hover on User photos in Testimonial section in Home page
  $(".testimonial-module .head-row ul li .head-img").hover(function(){
    var index = $(this).parents(".testimonial-module .head-row ul").find(".head-img").index($(this));

    $(this).parents(".testimonial-module .head-row ul").find(".head-img.active").removeClass("active");
    $(this).addClass("active");

    $(this).parents(".testimonial-module").find(".info-area").addClass("hide");
    $(this).parents(".testimonial-module").find(".info-area").eq(index).removeClass("hide");
  });

  //loading Home page
  if($(".home-page-content").length>0)
  {
    $("#video-player").mediaelementplayer({
        flashScriptAccess: 'always',
        loop: true
    });
  }


  //scroll Home page
  //scroll to page to show/hide top bar
  var loading_blog_content = false;
  $(document).scroll(function(){
    if($(".home-page-content").length>0)
    {
      //scroll to How it works section
      if($(window).scrollTop()+1>=($(".active-projects-module").offset().top) ){
        if(!$("header").hasClass("after-scroll-header"))
        {
          $("header").removeClass("top-section-header").addClass("after-scroll-header");
          $("header").hide();
          $(".logo-home").css("background",'url(/static/images/logo.png) no-repeat');
          $("header").slideDown();
        }
      }
      else
      {
        if($("header").hasClass("after-scroll-header"))
        {
          $("header").slideUp();
          setTimeout(function(){
            $("header").removeClass("after-scroll-header").addClass("top-section-header");
            $(".logo-home").css("background",'url(/static/images/logo-white.png) no-repeat');
            $("header").show();
          },500);
        }
      }
    }

    //scroll down to show more contents in Blog page
    if($(".blog-page-content").length>0)
    {
      if($(window).scrollTop()+1>=($(".grid-area").offset().top-$(window).height()+$(".grid-area").height()) ){
        if(!loading_blog_content)
        {
          loading_blog_content = true;
          $(".loading-bar").removeClass("hide");
          setTimeout(function(){
            var first_page_content;
            for(var i=0;i<2;i++)
            {
              first_page_content = $(".grid-area").find(".col-md-6").eq(0).clone(true).removeClass("hide");
              $(".grid-area").append(first_page_content);
            }
            $(".loading-bar").addClass("hide");
            loading_blog_content = false;
          },3000)
        }
      }
    }
  });

    //click tabs
  $(".mains-tabs .tab-index .row a").click(function(){
    var index = $(this).parents(".mains-tabs .tab-index").find(".row a").index($(this));

    $(this).parents(".mains-tabs .tab-index").find(".row a").removeClass("active");
    $(this).addClass("active");

    $(this).parents(".mains-tabs").find(".tab-content .tab-content-section").removeClass("active");
    $(this).parents(".mains-tabs").find(".tab-content .tab-content-section").eq(index).addClass("active");
  })

  //click on Login button in Sign In page
  $(".btn-login").click(function(){
    var pass = true;
    for(var i=0;i<$("input.required-input").length;i++)
    {
      if($("input.required-input").eq(i).val() === "")
      {
        $("input.required-input").eq(i).parent().addClass("input-error-style");
        pass = false;
      }
      else
      {
        $("input.required-input").eq(i).parent().removeClass("input-error-style");
      }
    }

    if(pass)
    {
      location.href = "home.html";
    }
  })

  //click on Sign Up button in Sign Up page
  $(".btn-signup").click(function(){
    var pass = true;
    for(var i=0;i<$("input.required-input").length;i++)
    {
      if($("input.required-input").eq(i).val() === "")
      {
        $("input.required-input").eq(i).parent().addClass("input-error-style");
        pass = false;
      }
      else if($("input.required-input").eq(i).hasClass("email-format"))
      {
        if(!checkMail($("input.required-input").eq(i).val()))
        {
          $("input.required-input").eq(i).parent().addClass("input-error-style");
          pass = false;
        }
        else
        {
          $("input.required-input").eq(i).parent().removeClass("input-error-style");
        }
      }
      else if($("input.required-input").eq(i).hasClass("password-match"))
      {
        if($("input.required-input").eq(i).val() !== $("input.required-input").eq(i-1).val())
        {
          $("input.required-input").eq(i).parent().addClass("input-error-style");
          pass = false;
        }
        else
        {
          $("input.required-input").eq(i).parent().removeClass("input-error-style");
        }
      }
      else
      {
        $("input.required-input").eq(i).parent().removeClass("input-error-style");
      }
    }

    if(!$(".required-checkbox").prev().hasClass("jqTransformChecked"))
    {
      pass = false;
    }

    if(pass)
    {
      location.href = "home.html";
    }
  })

  //check Email format
  function checkMail(mail){
    var filter  = /^([a-zA-Z0-9_\.\-])+\@(([a-zA-Z0-9\-])+\.)+([a-zA-Z0-9]{2,4})+$/;
    if (filter.test(mail))
      return true;
    else
    {
      return false;
    }
  }

  //focus on input box in Sign In/Sign Up pages
  $("input.required-input").focus(function(){
    $(this).parent().removeClass("input-error-style");
  })

  //click Enter key
  $(document).keydown(function(event){
    if(event.keyCode===13){
      if($(".btn-login").length>0)
      {
        $(".btn-login").click();
      }

      if($(".btn-signup").length>0)
      {
        $(".btn-signup").click();
      }
    }
  });

  //load google map
  if($("#map-canvas").length>0)
  {
    loadMap();
  }

  //load the google map
  function loadMap(){
    function initialize() {
      var myLatlngCenter = new google.maps.LatLng(-22.363882,131.044922);
      var mapOptions = {
        zoom: 4,
        center: myLatlngCenter,
        mapTypeControl: false
      };
      var map = new google.maps.Map(document.getElementById('map-canvas'), mapOptions);
      var myLatlng = new google.maps.LatLng(-22.363882,131.044922);

      var marker = new google.maps.Marker({
        position: myLatlng,
        map: map
      });
    }

    initialize();
  }
})
