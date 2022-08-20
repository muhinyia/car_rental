// Get the current year for the copyright
$("#year").text(new Date().getFullYear());

// fading alerts out
setTimeout(function () {
  $("#message").fadeOut("slow");
}, 3000);

// Get the current year for the copyright
$("#year").text(new Date().getFullYear());
//init scrollspy
$("body").scrollspy({ target: "#main-nav" });
//configure slider
$(".carousel").carousel({
  interval: 3000,
  pause: "hover",
});

// add smooth scrolling
$("#main-nav a").on("click", function (e) {
  //check for a hash value
  if (this.hash !== "") {
    //prevent default behaviour
    e.preventDefault();
    // store hash
    const hash = this.hash;

    //animate smoothscroll
    $("html,body").animate(
      {
        scrollTop: $(hash).offset().top,
      },
      900,
      function () {
        //add hash to URL after scroll
        window.location.hash = hash;
      }
    );
  }
});
//configure slider
$(".carousel").carousel({
  interval: 5000,
  pause: "hover",
});

// Lightbox Init
$(document).on("click", '[data-toggle="lightbox"]', function (event) {
  event.preventDefault();
  $(this).ekkoLightbox();
});
