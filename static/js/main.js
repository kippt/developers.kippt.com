/* Screenshot modal using Responsive Slideshow */

$(function () {
  
  // Copy the screenshots  
  $('.screenshots').clone().appendTo('#slider-inner').addClass('rslides');

  // Init slideshow
  $("#slider-wrapper .rslides").responsiveSlides({
    auto: false,
    pager: false,
    nav: true,
    speed: 500,
    namespace: "centered-btns"
  });

  // Open the slideshow
  $(".screenshots li").on("click", function(e){
      e.preventDefault();
      $("#slider-wrapper").fadeIn();
  });
  
  // Close the slideshow
  $(".close").on("click", function(e){
      e.preventDefault();
      $("#slider-wrapper").fadeOut();
  });
  
});