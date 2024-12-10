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