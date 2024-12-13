// admin.js
const api_status = {
  'category': false,
  'areacode': false,
  'sigungucode': false,
  'place': false,
  'event': false
}

document.addEventListener("DOMContentLoaded", () => {
  const tabs = document.querySelectorAll(".tabs li");
  const contents = document.querySelectorAll(".tab-content");

  tabs.forEach((tab) => {
      tab.addEventListener("click", () => {
          tabs.forEach((t) => t.classList.remove("active"));
          contents.forEach((c) => c.classList.remove("active"));

          tab.classList.add("active");
          if (tab.dataset.tab == '/') {
            return;
          }
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
  if (Object.values(api_status).some(value => value === true)) {
    return false;
  }
  if($('#AreaCode-'+areaCode).find('#place').children().length == 0){
    api_status['place'] = true
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
              <td><a href='/place/local/${areaCode}/view/${data.areaCode[i].place_id}' target="_blank">${data.areaCode[i].title}</a></td>
              <td>${data.areaCode[i].address}</td>
              <td><button class="open-place-modal">수정하기</button></td>
            </tr>
            `
          }
          $('#AreaCode-'+areaCode).find('#place').html(li_data)
      },
      error:function(){
          alert('실패')
      },
      complete: function() {
        api_status['place'] = false;
      }
    }) // ajax
  }

}

// 이벤트
function get_event_data(areaCode) {
  let csrfToken = $('meta[name=csrf_token]').attr('content')
  if (Object.values(api_status).some(value => value === true)) {
    return false;
  }
  if($('#event-AreaCode-'+areaCode).find('#place').children().length == 0){
    api_status['event'] = true
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
              <td><a href='/place/local/${areaCode}/view/${data.event[i].place_id}' target="_blank">${data.event[i].title}</a></td>
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
      },
      complete: function() {
        api_status['event'] = false;
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

  var email;
  var user_modi_content; // place 수정 정보 데이터

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
    
    user_modi_content = $(this).closest('tr').children()
    email = user_modi_content.eq(0).text()
    // ajax 요청
    $.ajax({
      headers:{'X-CSRFToken':csrfToken}, // scrf_token
      url:'/touradmin/get_user_view/', // 보내는 주소
      type:'post', // get, post // 서버쪽으로 보내는 변수데이터
      data:{'email':email},
      success:function(data){ // 서버에서 받은 데이터 : data
          if(data.result == 'success'){
            let viewData = JSON.parse(data.view)
            $('#username').val(viewData[0].fields.name)
            $('#nicname').val(viewData[0].fields.nickname)
            $('#user_address').val(viewData[0].fields.address)
          }
      },
      error:function(){
          alert('실패')
      }
    }) // ajax
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

$('#upload-btn').click(function() {
  let csrfToken = $('meta[name=csrf_token]').attr('content')
  var formData = new FormData();
  var fileInput = $('#image-upload')[0].files[0];
  if (fileInput) {
      formData.append('image', fileInput);

      $.ajax({
          headers:{'X-CSRFToken':csrfToken},
          url: "/touradmin/upload-image/",
          type: 'POST',
          data: formData,
          processData: false,
          contentType: false,
          success: function(response) {
              if (response.success) {
                  // 새로운 배너 이미지 테이블에 추가
                  var banner = response.image;
                  $('#banner-list').append(
                      '<tr>' +
                          '<td>' + banner.name + '</td>' +
                          '<td><img src="' + banner.path + '" style="width: 30px; height: 30px;" alt="Banner Image"></td>' +
                          '<td>' + banner.path + '</td>' +
                          '<td><button>활성화</button></td>' +
                      '</tr>'
                  );
                  // 파일 업로드 후 입력 필드 초기화
                  $('#image-upload').val('');
              } else {
                  alert('파일 업로드 실패');
              }
          },
          error: function() {
              alert('파일 업로드 중 오류가 발생했습니다.');
          }
      });
  } else {
      alert('파일을 선택해주세요.');
  }
});

// 이미지 삭제
$('.delete-btn').click(function() {
  let csrfToken = $('meta[name=csrf_token]').attr('content')
  var bannerId = $(this).closest('tr').attr('id');  // 삭제할 배너 ID를 가져옵니다
  var bannerpath = $(this).closest('tr').children().eq(2).text();  // 패스
  // 사용자에게 확인을 요청
  if (confirm('정말로 이 배너 이미지를 삭제하시겠습니까?')) {
      $.ajax({
          headers:{'X-CSRFToken':csrfToken},
          url: '/touradmin/delete-image/',  // 삭제할 이미지의 ID를 URL에 추가
          data: {'bannerId':bannerpath},
          type: 'POST',
          success: function(response) {
              if (response.success) {
                  // 삭제가 성공하면 해당 배너 항목을 테이블에서 제거
                  $('#' + bannerId).remove();
                  alert('배너 이미지가 삭제되었습니다.');
              } else {
                  alert('배너 이미지 삭제에 실패했습니다.');
              }
          },
          error: function() {
              alert('서버 오류로 배너 이미지를 삭제할 수 없습니다.');
          }
      });
  }
});

// 이미지 활성화
$(document).on('click', '#active_banner', function(){
  if(confirm('활성화 됩니다.')){
    var image_title = $(this).closest('tr').children().eq(0).text()
    var image_path = $(this).closest('tr').children().eq(2).text()
    var bannerId = $(this).closest('tr').attr('id');
    
    let csrfToken = $('meta[name=csrf_token]').attr('content')
    $.ajax({
      headers:{'X-CSRFToken':csrfToken},
      url: '/touradmin/active_banner/',  // 삭제할 이미지의 ID를 URL에 추가
      data: {'title':image_title, 'path':image_path},
      type: 'POST',
      success: function(response) {
          if (response.success) {
              // 삭제가 성공하면 해당 배너 항목을 테이블에서 제거
              $('#' + bannerId).remove();
              $('#act_list').append(
                '<tr>' +
                  '<td>' + image_title + '</td>' +
                  '<td><img src="' + image_path + '" style="width: 30px; height: 30px;" alt="Banner Image"></td>' +
                  '<td>' + image_path + '</td>' +
                  '<td><button id="deactive_banner">비활성화</button></td>' +
                '</tr>'
              )
              alert('활성화 되었습니다.');
          } else {
              alert('활성화 실패 했습니다..');
          }
      },
      error: function() {
          alert('서버 오류로 배너 이미지를 활성화할 수 없습니다.');
      }
  });

  }
})

$(document).on('click', '#deactive_banner', function(){
  if(confirm('비활성화 됩니다.')){
    var image_no = $(this).closest('tr').attr('id')
    var datapath = $(this).closest('tr').children()

    let csrfToken = $('meta[name=csrf_token]').attr('content')
    $.ajax({
      headers:{'X-CSRFToken':csrfToken},
      url: '/touradmin/deactive_banner/',  // 삭제할 이미지의 ID를 URL에 추가
      data: {'id':image_no},
      type: 'POST',
      success: function(response) {
          if (response.success) {
              // 삭제가 성공하면 해당 배너 항목을 테이블에서 제거
              datapath.eq(3).prop('checked', false);
              alert('비활성화 되었습니다.');
          } else {
              alert('비활성화 실패 했습니다..');
          }
      },
      error: function() {
          alert('서버 오류로 배너 이미지를 비활성화할 수 없습니다.');
      }
   });

  }
})