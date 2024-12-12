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
              <td>${data.areaCode[i].address}</td>
              <td><button class="open-place-modal">수정하기</button></td>
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
          var li_data = ''
          for(let i = 0; i < data.event.length; i++){
            li_data += `
            <tr id='${areaCode}_${i}'>
              <td>${data.event[i].place_id}</td>
              <td>${data.event[i].title}</td>
              <td>${data.event[i].address}</td>
              <td>${data.event[i].start_time} - ${data.event[i].end_time}</td>
              <td><button class="open-place-modal">수정하기</button></td>
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

// 모달
document.addEventListener('DOMContentLoaded', function() {
  // place
  var placemodal = document.getElementById("place-modal");
  var placespan = document.getElementsByClassName("place-close")[0];
  // user
  var usermodal = document.getElementById("editProfileModal");
  var userspan = document.getElementsByClassName("user-modal-close-btn")[0];

  var no; // place 수정 번호
  var modi_content; // place 수정 정보 데이터
  let csrfToken = $('meta[name=csrf_token]').attr('content')

  // place 열기
  $(document).on('click', '.open-place-modal', function(){
    placemodal.style.display = "block";
    var modi_no = $(this).closest('tr').attr('id')
    $('#modi_No').html(modi_no+' 번 수정')

    // ajax 요청
    modi_content = $(this).closest('tr').children()
    no = modi_content.eq(0).text()

    $.ajax({
      headers:{'X-CSRFToken':csrfToken}, // scrf_token
      url:'/touradmin/get_view/', // 보내는 주소
      type:'post', // get, post // 서버쪽으로 보내는 변수데이터
      data:{'no':no},
      success:function(data){ // 서버에서 받은 데이터 : data
          if(data.result != 'fail'){
            let viewData = JSON.parse(data.view)
            $('#title').val(viewData[0].fields.title)
            $('#address').val(viewData[0].fields.address)
            $('#tel').val(viewData[0].fields.tel)
            $('#image').val(viewData[0].fields.image)
            $('#thumb_img').val(viewData[0].fields.thumb_img)
            $('#homepage_url').val(viewData[0].fields.homepage_url)
            $('#overview').val(viewData[0].fields.overview)
          }
      },
      error:function(){
          alert('실패')
      }
    }) // ajax
  })

  // place 데이터 수정하기
  $(document).on('click', '.sumBut', function(){
    // 수정 데이터 확인
    if(confirm('수정 하시겠습니까?')){
      var target = no
      var title = $('#title').val()
      var address = $('#address').val()
      var tel = $('#tel').val()
      var image = $('#image').val()
      var thumb_img = $('#thumb_img').val()
      var homepage_url = $('#homepage_url').val()
      var overview = $('#overview').val()
  
      // ajax
      $.ajax({
        headers:{'X-CSRFToken':csrfToken}, // scrf_token
        url:'/touradmin/update/', // 보내는 주소
        type:'post', // get, post // 서버쪽으로 보내는 변수데이터
        data:{'target':target, 'title':title, 'address':address,
          'tel':tel, 'image':image, 'thumb_img':thumb_img,
          'homepage_url':homepage_url, 'overview':overview
        },
        success:function(data){ // 서버에서 받은 데이터 : data
            if(data.result == 'success'){
              let viewData = JSON.parse(data.view)
              modi_content.eq(1).text(viewData[0].fields.title)
              modi_content.eq(2).text(viewData[0].fields.thumb_img)
              modi_content.eq(3).text(viewData[0].fields.image)
            }
        },
        error:function(){
            alert('실패')
        }
      }) // ajax
    }// confirm
    placemodal.style.display = 'none';
  })

  // user 열기
  $(document).on('click', '.user-btn', function(){
    usermodal.style.display = "flex";

    // ajax 요청
    modi_content = $(this).closest('tr').children()
  })

  // user 데이터 수정
  $(document).on('click', '.user-modibtn', function(){
    // 수정 데이터 확인
    usermodal.style.display = 'none';
  })

  // place 모달창 닫기
  placespan.onclick = function() {
    placemodal.style.display = "none";
  }
  // user 모달창 닫기
  userspan.onclick = function() {
    usermodal.style.display = "none";
  }

  // place
  window.onclick = function(event) {
    if (event.target == usermodal || event.target == placemodal) {
      usermodal.style.display = "none";
      placemodal.style.display = "none";
    }
  }
});
