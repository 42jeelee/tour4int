$(function () {
  const areaboxs = $(".itemlist > .areabox");

  /*
  * {
  *   isEnd: bool,
  *   distance: int,
  * }
  * */
  function getDistance(screenWidth, itemList, isPrev) {
    const currLeft = parseInt(itemList.css("left"));
    const itemLen = itemList.children().length;
    
    let result = { isEnd: false, distance: currLeft }
    if (itemLen > 0) {
      const firstItem = itemList.children().first();
      const itemWidth = firstItem.outerWidth();
      const itemMargin = parseInt(firstItem.css("margin-right"));

      const shownItems = currLeft / (itemWidth + itemMargin);
      const visibleItems = screenWidth / (itemWidth + itemMargin);
      const remainItems = shownItems + itemLen - visibleItems;
      
      if (isPrev) {
        const moveValue = shownItems > visibleItems? shownItems : visibleItems;
        result.distance += (itemWidth + itemMargin) * moveValue;

        if (result.distance >= 0) {
          result.distance = 0;
          result.isEnd = true;
        }
      } else {
        const fullDistance = (itemWidth + itemMargin) * (itemLen - visibleItems) * -1;
        const moveValue = remainItems < visibleItems? remainItems : visibleItems;
        result.distance -= (itemWidth + itemMargin) * moveValue;

        if (result.distance <= fullDistance) {
          result.distance = fullDistance;
          result.isEnd = true;
        }
      }
    }
    
    return result;
  }

  function needBtns(screen) {
    const screenWidth = screen.outerWidth();
    const itemlist = screen.find(".itemlist");
    const itemlistWidth = itemlist.outerWidth();
    
    return itemlistWidth > screenWidth;
  }

  $(document).on("click", ".item-screen__btn", function() {
    const btns = $(this).parent().children();
    const isPrev = $(this).hasClass("prev-btn");
    
    const itemscreen = $(this).closest(".item-screen");
    const screenWidth = itemscreen.outerWidth();
    const itemList = itemscreen.find(".itemlist");
    
    const moveDistance = getDistance(screenWidth, itemList, isPrev);

    itemList.animate({ left: moveDistance.distance + "px"}, 500, "swing");

    btns.removeClass("disable-btn");

    if (moveDistance.isEnd) {
      if (isPrev) {
        btns.first().addClass("disable-btn");
      } else {
        btns.eq(1).addClass("disable-btn");
      }
    }
  });

  $(document).on("click", ".areabox__btn", function() {
    const area_code = $(this).closest(".areabox").attr("id");

    location.href = `/place/local/${area_code}/`;
  });

  $(".item-screen__btns").each(function() {
    const screen = $(this).closest(".item-screen");
    
    if (needBtns(screen)) {
      $(this).children(".item-screen__btn").eq(1).removeClass("disable-btn");
    }
  })

});