document.addEventListener('DOMContentLoaded', function() {
  const tabs = document.querySelectorAll('.near_tap .near_btn');
  const contents = document.querySelectorAll('.tap_body');

  tabs.forEach(tab => {
    tab.addEventListener('click', function(e) {
      e.preventDefault();
      
      // 모든 탭과 내용에서 active 클래스 제거
      tabs.forEach(t => t.classList.remove('active'));
      contents.forEach(c => c.classList.remove('active'));
      
      // 클릭된 탭과 해당 내용에 active 클래스 추가
      this.classList.add('active');
      const targetId = this.getAttribute('href').substring(1);
      document.getElementById(targetId).classList.add('active');
    });
  });
});

// 좋아요
document.querySelectorAll('.like-button').forEach(button => {
  button.addEventListener('click', function () {
      const postId = this.getAttribute('data-post-id');
      const isLiked = this.getAttribute('data-liked') === 'true';

      // 버튼 클릭 시 비활성화 (중복 클릭 방지)
      this.disabled = true;

      fetch(`/place/like/${postId}/`, {
          method: 'POST',
          headers: {
              'X-CSRFToken': csrfToken = $('meta[name=csrf_token]').attr('content'),
              'Content-Type': 'application/json'
          },
          body: JSON.stringify({ liked: !isLiked })
      })
      .then(response => response.json())
      .then(data => {
          this.textContent = data.liked ? '좋아요 취소' : '좋아요';
          this.setAttribute('data-liked', data.liked);
          document.querySelector(`#like-count`).textContent = `${data.like_count}명이 좋아요를 눌렀습니다.`;
      })
      .catch(error => {
          console.error('Error:', error);
          alert('좋아요 처리 중 오류가 발생했습니다.');
      })
      .finally(() => {
          // 버튼 클릭 후 비활성화 해제
          this.disabled = false;
      });
  });
});

$('.not_login').click(function(){
  alert('좋아요는 로그인을 하셔야 합니다.')
})

  // 그래프
function renderChart(canvas, stats){
    if (canvas == null) return false
    if (stats == null){
        let chartStatus2 = Chart.getChart("commentsChart");
        if (chartStatus2 != undefined ) chartStatus2.destroy();
        return false
    }
    let chartStatus = Chart.getChart("commentsChart"); // <canvas> id
    if (chartStatus != undefined) {
        chartStatus.destroy();
        canvas = document.getElementById('commentsChart');
    }
    var ctx = canvas.getContext("2d");
    new Chart(ctx, {
    type: 'bar',
    data: {
        labels: ['유모차 대여', '신용카드 사용', '애완동물 동반', '주차 시설', '화장실', '엘리베이터', '휠체어 통로', '휠체어 대여'],
        datasets: [{
            label: '있음 비율 (%)',
            data: [
                stats.stroller_rental,
                stats.credit_card,
                stats.pet_friendly,
                stats.parking,
                stats.restroom,
                stats.elevator,
                stats.wheelchair_path,
                stats.wheelchair_rental
            ],
            backgroundColor: 'rgba(54, 162, 235, 0.2)',
            borderColor: 'rgba(54, 162, 235, 1)',
            borderWidth: 1
        }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true,
                    max: 100
                }
            }
        }
    });
}