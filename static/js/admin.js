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

// 지역
function get_place_data(areaCode) {
  let csrfToken = $('meta[name=csrf_token]').attr('content')
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
            <tr id='${areaCode}_${i}'>
              <td>${data.areaCode[i].place_id}</td>
              <td>${data.areaCode[i].title}</td>
              <td>${data.areaCode[i].thumb_img}</td>
              <td>${data.areaCode[i].image}</td>
              <td><button class='modBut'>수정하기</button></td>
            </tr>
            <tr id='${data.areaCode[i].place_id}' class='modi no_display'>
              <td>${data.areaCode[i].place_id}</td>
              <td><input id='${data.areaCode[i].place_id}_title' type='text' value='${data.areaCode[i].title}'></td>
              <td><input id='${data.areaCode[i].place_id}_thumb_img' type='text' value='${data.areaCode[i].thumb_img}'></td>
              <td><input id='${data.areaCode[i].place_id}_image' type='text' value='${data.areaCode[i].image}'></td>
              <td><button class='sumBut'>적용하기</button></td>
            </tr>
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

// 이벤트
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
            <tr id='${areaCode}_${i}'>
              <td>${data.event[i].place_id}</td>
              <td>${data.event[i].title}</td>
              <td>${data.event[i].thumb_img}</td>
              <td>${data.event[i].image}</td>
              <td><button class='modBut'>수정하기</button></td>
            </tr>
            <tr id='${data.event[i].place_id}' class='modi no_display'>
              <td>${data.event[i].place_id}</td>
              <td><input id='${data.event[i].place_id}_title' type='text' value='${data.event[i].title}'></td>
              <td><input id='${data.event[i].place_id}_thumb_img' type='text' value='${data.event[i].thumb_img}'></td>
              <td><input id='${data.event[i].place_id}_image' type='text' value='${data.event[i].image}'></td>
              <td><button class='sumBut'>적용하기</button></td>
            </tr>
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

$(document).on('click', '.modBut', function(){
  // 모든 modi가져와서 active 되있는거 꺼주기
  var all_modi = document.querySelectorAll('.modi')
  all_modi.forEach((c) => c.classList.add("no_display"))

  // 현제 누른 tr 다음거 활성화 하기
  var test = $(this).closest('tr').attr('id')
  $(this).closest('tr').next().removeClass('no_display')
})

$(document).on('click', '.sumBut', function(){
  // 수정 데이터 확인
  var modi_id = $(this).closest('tr').attr('id')
  var modi_title = $('#' + modi_id + '_title').val()
  var modi_thumb_img = $('#' + modi_id + '_thumb_img')
  var modi_image = $('#' + modi_id + '_image')
  console.log(modi_id + ' : ' + modi_title)
})