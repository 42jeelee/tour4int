$(function() {
  const headerBar = $("header > .header__container:first-child > .header__container--wrap");
  
  let lastScrollTime = 0;
  let throttleDelay = 10;

  $(window).on('scroll', function() {
    const now = new Date().getTime();
    if (now - lastScrollTime >= throttleDelay) {
      lastScrollTime = now;
      const currTop = $(window).scrollTop();

      if (currTop > 500) headerBar.addClass("search-header");
      else headerBar.removeClass("search-header");
      if (currTop > 60) {
        headerBar.addClass("fixed-top");
      } else {
        headerBar.removeClass("fixed-top");
      }
    }
  });
});