$(function() {
  const headerBar = $("header > .header__container:first-child > .header__container--wrap");
  const main = $("main");
  const sideBar = main.find("div.wrap > .side-bar");
  const mainTop = main.offset().top;
  const sideBarEnd = main.outerHeight() - sideBar.outerHeight();
  const screenHeight = window.innerHeight;
  const sideBarBottom = sideBar.outerHeight() + 100;

  let sideBarTop = $(window).scrollTop() + screenHeight - mainTop - sideBarBottom;
  sideBar.css("top", sideBarTop + "px");

  let lastScrollTime = 0;
  let throttleDelay = 10;
  
  $(window).on('scroll', function() {
    const now = new Date().getTime();

    if (now - lastScrollTime >= throttleDelay) {
      lastScrollTime = now;
      const currTop = $(window).scrollTop();

      
      if (currTop > 60) {
        headerBar.addClass("fixed-top");
        
        if (currTop > mainTop) headerBar.addClass("search-header");
        else headerBar.removeClass("search-header");
        
      } else headerBar.removeClass("fixed-top");

      sideBarTop = currTop + screenHeight - mainTop - sideBarBottom;
      if (sideBarTop > sideBarEnd) sideBarTop = sideBarEnd;
      else if (sideBarTop < 0) sideBarTop = 0;

      sideBar.css("top", sideBarTop + "px");

    }
  });
});