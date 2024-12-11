// admin.js
document.addEventListener("DOMContentLoaded", () => {
  const tabs = document.querySelectorAll(".tabs li");
  const contents = document.querySelectorAll(".tab-content");

  tabs.forEach((tab) => {
      tab.addEventListener("click", () => {
          tabs.forEach((t) => t.classList.remove("active"));
          contents.forEach((c) => c.classList.remove("active"));

          tab.classList.add("active");
          document.getElementById(tab.dataset.tab).classList.add("active");
      });
  });
});

document.addEventListener("DOMContentLoaded", () => {
  // 서브탭 활성화 기능
  const subTabs = document.querySelectorAll(".sub-tabs li");
  const subTabContents = document.querySelectorAll(".sub-tab-content");

  subTabs.forEach(tab => {
      tab.addEventListener("click", () => {
          // 모든 서브탭에서 active 클래스 제거
          subTabs.forEach(t => t.classList.remove("active"));
          // 모든 컨텐츠 숨기기
          subTabContents.forEach(content => content.classList.remove("active"));

          // 클릭된 탭에 active 클래스 추가
          tab.classList.add("active");
          const targetId = tab.getAttribute("data-subtab");
          document.getElementById(targetId).classList.add("active");
      });
  });
});

function get_place_data(areaCode) {
  let csrfToken = $('meta[name=csrf_token]').attr('content')
  console.log($('#AreaCode-'+areaCode).find('#place').children().length)
  if($('#AreaCode-'+areaCode).find('#place').children().length == 0){
    $.ajax({
      headers:{'X-CSRFToken':csrfToken}, // scrf_token
      url:'/touradmin/get_place/', // 보내는 주소
      type:'post', // get, post
      data:{'areaCode':areaCode}, // 서버쪽으로 보내는 변수데이터
      success:function(data){ // 서버에서 받은 데이터 : data
          var li_data = ''
          for(let i = 0; i < data.areaCode.length; i++){
            li_data += `
            <li>${data.areaCode[i].title}</li>
            `
          }
          $('#AreaCode-'+areaCode).find('#place').html(li_data)
      },
      error:function(){
          alert('실패')
      }
    }) // ajax
  }

}

function get_event_data(areaCode) {
  let csrfToken = $('meta[name=csrf_token]').attr('content')
  
  if($('#event-AreaCode-'+areaCode).find('#place').children().length == 0){
    $.ajax({
      headers:{'X-CSRFToken':csrfToken}, // scrf_token
      url:'/touradmin/get_event/', // 보내는 주소
      type:'post', // get, post
      data:{'areaCode':areaCode}, // 서버쪽으로 보내는 변수데이터
      success:function(data){ // 서버에서 받은 데이터 : data
          console.log('성공 여부 : ' + data.result)
          var li_data = ''
          for(let i = 0; i < data.event.length; i++){
            li_data += `
            <li>${data.event[i].title}</li>
            `
          }
          $('#event-AreaCode-'+areaCode).find('#place').html(li_data)
      },
      error:function(){
          alert('실패')
      }
    }) // ajax
  }

}