$(function() {
  const headerBar = $("header > .header__container:first-child > .header__container--wrap");
  const main = $("main");
  const sideBar = main.find("div.wrap > .side-bar");
  const mainTop = main.offset().top;
  const screenHeight = window.innerHeight;
  const sideBarBottom = sideBar.outerHeight() + 100;
  
  sideBar.css("top", getSideBarTop() + "px");
  
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
      
      sideBar.css("top", getSideBarTop(currTop) + "px");
    }
  });
  
  function getSideBarTop(currTop=$(window).scrollTop()) {
    const sideBarEnd = main.outerHeight() - sideBar.outerHeight();

    let sideBarTop = currTop + screenHeight - mainTop - sideBarBottom;

    if (sideBarTop > sideBarEnd) sideBarTop = sideBarEnd;
    else if (sideBarTop < 0) sideBarTop = 0;

    return sideBarTop;
  }

  $(".side-bar__btn").click(function() {
    if ($(this).hasClass("btn-up")) $('html').animate({ scrollTop: 0 }, 200);
    else $('html').animate({ scrollTop: $(document).height() }, 200);
  });

  $(".side-bar__content").click(function(e) {
    const cid = $(this).attr("id");
    
    $(".side-bar__content").each(async function() {
      const item = $(this);
      const ccid = item.attr("id");

      if (item.hasClass("active")) {
        if (cid !== ccid ||
          $(e.target).is(".side-bar__content--container-cancel") ||
          $(e.target).is(".side-bar__content--icon")) {
            item.find(".side-bar__content--container").remove();
            item.removeClass("active");
          }
      } else if (cid === ccid) {
        const container = $("<div>", {
          class: "side-bar__content--container",
        });

        const items = await sideBarContentItems(ccid);

        if (items.length > 0) {
          
        }

        const itemCards = items.map(item => {
          const card = $("<div>", {
            id: item.id,
            class: "side-bar__content--card",
          });
  
          const cardBody = `
            <div class="card-wrap">
              <div class="card-img">
                <img src="${item.image}" />
              </div>
              <div class="card-area">${item.area}</div>
              <div class="card-title">${item.title}</div>
            </div>
          `;

          card.html(cardBody);
          return card;
        });

        const wrappedCard = wrappingCard(itemCards);

        const cancelBtn = $("<div>", {
          class: "side-bar__content--container-cancel",
        });

        const nextBtns = $("<div>", {
          class: "side-bar__content--btns",
        });

        nextBtns.html("<div class='side-bar__content--btn'></div><div class='side-bar__content--btn next'></div>")

        container.append(cancelBtn, wrappedCard, nextBtns);
        
        item.append(container);
        item.addClass("active");
        getSideBarBtnIdx(container, "active-card");
      }
    });
  });

  $(document).on("click", ".side-bar__content--btn", function() {
    const activeClassName = "active-card";
    const container = $(this).closest(".side-bar__content--container");
    const wrappers = container.children(".side-bar__content--wrap");
    const wrappersNum = wrappers.length;

    const activedIdx = getSideBarBtnIdx(container, activeClassName);

    if ($(this).hasClass("next")) {
      const nextIdx = activedIdx + 1;

      if (activedIdx >= wrappersNum - 1) return ;

      wrappers.eq(activedIdx).removeClass(activeClassName);
      wrappers.eq(nextIdx).addClass(activeClassName);
    } else {
      const prevIdx = activedIdx - 1;

      if (activedIdx <= 0) return ;
      
      wrappers.eq(activedIdx).removeClass(activeClassName);
      wrappers.eq(prevIdx).addClass(activeClassName);
    }

    getSideBarBtnIdx(container, activeClassName);
  });
  
  function getSideBarBtnIdx(container, activeClassName) {
    const btns = $(".side-bar__content--btn");
    const wrappers = container.children(".side-bar__content--wrap");
    const wrappersNum = wrappers.length;

    if (wrappersNum <= 1) {
      $(".side-bar__content--btn").remove();
      return ;
    }
    
    const activedIdx = wrappers.filter("." + activeClassName).index() - 1;

    btns.removeClass("disable-btn");

    if (activedIdx >= wrappersNum - 1) btns.eq(1).addClass("disable-btn");
    else if (activedIdx <= 0) btns.eq(0).addClass("disable-btn");

    return activedIdx;
  }

  function sideBarContentItems(cid) {
    if (cid === "side-history") {
      return new Promise((resolve, reject) => {
        $.ajax({
          url: "/accounts/history/all",
          type: "get",
          success: function(data) {
            const { result } = data;

            if (result === "success") {
              resolve(data.data);
            } else reject([]);
          },
          error: function(e) {
            console.log("실패 :", e);
            reject([]);
          }
        });
      });
    }
    return Promise.resolve([]);
  }

  function wrappingCard(items) {
    if (items.length > 0) {
      return items.reduce((acc, curr, idx) => {
        if (idx % 2 === 0) {
          const wrapper = $("<div>", {
            id: "card-page__" + idx,
            class: "side-bar__content--wrap",
          });
  
          if (idx === 0) wrapper.addClass("active-card");
  
          const pair = [curr];
  
          if (items[idx + 1] !== undefined) pair.push(items[idx + 1]);
  
          wrapper.append(pair);
          acc.push(wrapper);
        }
        return acc;
      }, []);
    }
    const wrapper = $("<div>", {
      id: "card-page__0",
      class: "side-bar__content--wrap active-card",
    });

    const emptyItem = $("<div>", {
      class: "side-bar__content--empty",
      text: "목록이 존재하지 않습니다.",
    });

    wrapper.append(emptyItem);
    return [wrapper];
  }

  $(document).on("click", ".side-bar__content--card", function() {
    const itemId = $(this).attr("id");

    location.href = `/place/local/1/view/${itemId}`;
  });
});