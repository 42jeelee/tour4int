$(function() {
  const categoryBox = $("#dataSetting #data-item__category");
  const areacodeBox = $("#dataSetting #data-item__areacode");
  const sigungucodeBox = $("#dataSetting #data-item__sigungucode");
  
  const data_listBox = $("#dataSetting .data-list:last-child");
  const placeBox = $("#dataSetting #data-item__place");
  const eventBox = $("#dataSetting #data-item__event");
  const prefix = "data-item__";


  $("li[data-tab='dataSetting']").click(function() {
    if (Object.values(api_status).includes(true)) return ;
    $.ajax({
      url: "/api/get_logged/",
      type: "get",
      success: function(data) {
        settingAllBox(data);
      },
      error: function(e) {
        console.log("error :", e);
      }
    });
  });

  $(document).on("click", ".data-item.active-btn > .data-item__content", function() {
    const item = $(this).closest(".data-item");
    const itemId = item.attr("id");

    if (itemId.startsWith(prefix)) {
      const boxId = itemId.substring(prefix.length);

      if (!(boxId === "place" || boxId === "event")) {

        if (((placeBox.hasClass("fetched") || eventBox.hasClass("fetched")) ||
          (boxId === "areacode" && sigungucodeBox.hasClass("fetched"))) &&
          !confirm("값을 다시 불러오는 경우 의존하는 데이터들도 모두 지워집니다.\n계속하시겠습니까?")) {
          return ;
        }
      }
      if (isLoadingChild(boxId)) {
        alert("의존하는 데이터가 로드중입니다.");
        return ;
      }
      fetchData(boxId);
    }
  });

  function isActiveBtn(boxId) {
    return (boxId == "category" || boxId == "areacode") ||
    (boxId == "sigungucode" && areacodeBox.hasClass("fetched")) ||
    ((boxId == "place" || boxId == "event") &&
    sigungucodeBox.hasClass("fetched") && categoryBox.hasClass("fetched"));
  }

  function isLoadingChild(boxId) {
    if (boxId == "place" || boxId == "event") return false;
    if (boxId == "category" || boxId == "sigungucode") return api_status['place'] || api_status['event'];
    if (boxId == "areacode") return api_status['sigungucode'] || api_status['place'] || api_status['event'];
    return false;
  }

  function loadingItem(itemBox, boxId) {
    if (api_status[boxId]) {
      itemBox.removeClass("active-btn fetched");
      itemBox.addClass("load-item");
      return true;
    } else {
      itemBox.removeClass("load-item");
    }
    return false;
  }

  function settingItemBox(itemBox, data) {
    const { fetched, modify_date, data_num } = data;
    const DAY_STRING = ['일', '월', '화', '수', '목', '금', '토'];
    const boxDate = itemBox.find(".data-item__modify");
    const boxNum = itemBox.find(".data-item__num");
    const boxId = itemBox.attr("id").substring(prefix.length);

    if (loadingItem(itemBox, boxId)) return;

    if (!fetched) {
      boxDate.text("");
      boxNum.text("");
      itemBox.removeClass("fetched");

      if (isActiveBtn(boxId)) itemBox.addClass("active-btn");
      else itemBox.removeClass("active-btn");

      return ;
    }

    const date = new Date(modify_date);
    const y = date.getFullYear();
    const m = date.getMonth() + 1;
    const d = date.getDate();
    const a = DAY_STRING[date.getDay()];

    boxDate.text(`${y}-${m}-${d} (${a})`);
    boxNum.text(`${data_num} 개`);

    itemBox.addClass("fetched");

    if (boxId === "areacode") sigungucodeBox.addClass("active-btn");
  }

  function settingAllBox(data) {
    const { category, areacode, sigungucode, place, event } = data;

    initial_items();

    settingItemBox(categoryBox, category);
    settingItemBox(areacodeBox, areacode);
    settingItemBox(sigungucodeBox, sigungucode);
    settingItemBox(placeBox, place);
    settingItemBox(eventBox, event);

    setting_placebox();
  }
  
  function fetchData(dataName) {
    const item = $("#"+prefix+dataName);
    
    api_status[dataName] = true;
    loadingItem(item, dataName);

    let path = `init_${dataName}`;
    if (dataName == "place" || dataName == "event") path = `get_${dataName}`;      
    else setting_placebox();

    $.ajax({
      url: `/api/${path}/`,
      type: "get",
      success: function(data) {
        const { result, log_info: logInfo } = data;
        
        api_status[dataName] = false;
        loadingItem(item, dataName);
        if (result === "success") settingAllBox(logInfo);
        else {
          alert("서버에 문제가 발생하였습니다.");
          initial_items(true);
        }
      },
      error: function(e) {
        api_status[dataName] = false;
        console.log("fail :", e);
        error_item(item);
      }
    });
  }

  function error_item(itemBox) {
    itemBox.removeClass("active-btn fetched load-item");
    itemBox.addClass("shake-item");
    
    setTimeout(() => {
      itemBox.removeClass("shake-item");
    }, 500);
  }

  function setting_placebox() {

    if (categoryBox.hasClass("fetched") && sigungucodeBox.hasClass("fetched")) {
      data_listBox.addClass("active-list");
      placeBox.addClass("active-btn");
      eventBox.addClass("active-btn");
      return ;
    }
    data_listBox.removeClass("active-list");
    placeBox.removeClass("load-item active-btn fetched");
    eventBox.removeClass("load-item active-btn fetched");
  }

  function initial_items(isError=false) {
    categoryBox.removeClass("load-item active-btn fetched");
    areacodeBox.removeClass("load-item active-btn fetched");
    sigungucodeBox.removeClass("load-item active-btn fetched");

    setting_placebox();

    if (!isError) {
      categoryBox.addClass("active-btn");
      areacodeBox.addClass("active-btn");
    }
  }

});