from django.db import models
from accounts.models import User
from areacode.models import SigunguCode
from category.models import Category

# Create your models here.
class Place(models.Model):
  place_id = models.IntegerField(primary_key=True)

  category = models.ForeignKey(Category, on_delete=models.CASCADE)
  sigungu_code = models.ForeignKey(SigunguCode, on_delete=models.CASCADE)

  title = models.CharField(max_length=100, null=False)
  address = models.CharField(max_length=100, null=False)
  map_x = models.CharField(max_length=20, null=False)
  map_y = models.CharField(max_length=20, null=False)
  
  tel = models.CharField(max_length=13)
  image = models.CharField(max_length=100)
  thumb_img = models.CharField(max_length=100)

  start_time = models.DateField(null=True)
  end_time = models.DateField(null=True)

  is_detail = models.BooleanField(default=False)
  homepage_url = models.CharField(max_length=500, null=True)
  overview = models.TextField(null=True)

  accomcount = models.CharField(max_length=255, null=True)
  chkbabycarriage = models.CharField(max_length=255, null=True)
  chkcreditcard = models.CharField(max_length=255, null=True)
  chkpet = models.CharField(max_length=255, null=True)
  expagerange = models.CharField(max_length=255, null=True)
  expguide = models.CharField(max_length=255, null=True)
  heritage1 = models.CharField(max_length=255, null=True)
  heritage2 = models.CharField(max_length=255, null=True)
  heritage3 = models.CharField(max_length=255, null=True)
  infocenter = models.CharField(max_length=255, null=True)
  opendate = models.CharField(max_length=255, null=True)
  parking = models.CharField(max_length=255, null=True)
  restdate = models.CharField(max_length=255, null=True)
  useseason = models.CharField(max_length=255, null=True)
  usetime = models.CharField(max_length=255, null=True)
  accomcountculture = models.CharField(max_length=255, null=True)
  chkbabycarriageculture = models.CharField(max_length=255, null=True)
  chkcreditcardculture = models.CharField(max_length=255, null=True)
  chkpetculture = models.CharField(max_length=255, null=True)
  discountinfo = models.CharField(max_length=255, null=True)
  infocenterculture = models.CharField(max_length=255, null=True)
  parkingculture = models.CharField(max_length=255, null=True)
  parkingfee = models.CharField(max_length=255, null=True)
  restdateculture = models.CharField(max_length=255, null=True)
  usefee = models.CharField(max_length=255, null=True)
  usetimeculture = models.CharField(max_length=255, null=True)
  scale = models.CharField(max_length=255, null=True)
  spendtime = models.CharField(max_length=255, null=True)
  agelimit = models.CharField(max_length=255, null=True)
  bookingplace = models.CharField(max_length=255, null=True)
  discountinfofestival = models.CharField(max_length=255, null=True)
  eventenddate = models.CharField(max_length=255, null=True)
  eventhomepage = models.CharField(max_length=255, null=True)
  eventplace = models.CharField(max_length=255, null=True)
  eventstartdate = models.CharField(max_length=255, null=True)
  festivalgrade = models.CharField(max_length=255, null=True)
  placeinfo = models.CharField(max_length=255, null=True)
  playtime = models.CharField(max_length=255, null=True)
  program = models.CharField(max_length=255, null=True)
  spendtimefestival = models.CharField(max_length=255, null=True)
  sponsor1 = models.CharField(max_length=255, null=True)
  sponsor1tel = models.CharField(max_length=255, null=True)
  sponsor2 = models.CharField(max_length=255, null=True)
  sponsor2tel = models.CharField(max_length=255, null=True)
  subevent = models.CharField(max_length=255, null=True)
  usetimefestival = models.CharField(max_length=255, null=True)
  distance = models.CharField(max_length=255, null=True)
  infocentertourcourse = models.CharField(max_length=255, null=True)
  schedule = models.CharField(max_length=255, null=True)
  taketime = models.CharField(max_length=255, null=True)
  theme = models.CharField(max_length=255, null=True)

  updated_at = models.DateTimeField(auto_now=True)
  created_at = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return f"{self.title} ({self.address})"
  
  @property
  def like_count(self):
      """좋아요 수 반환"""
      return self.likes.count()
  
class Like(models.Model):
  place = models.ForeignKey(Place, on_delete=models.CASCADE, related_name='likes')  # 어떤 게시물에 대한 좋아요인지
  user = models.ForeignKey(User, on_delete=models.CASCADE)  # 어떤 사용자가 좋아요를 눌렀는지
  created_at = models.DateTimeField(auto_now_add=True)  # 좋아요를 누른 시간

  class Meta:
      unique_together = ('place', 'user')  # 한 사용자가 같은 게시물에 좋아요를 중복으로 누르지 못하도록 설정

  def __str__(self):
      return f"{self.user.nickname} likes {self.place.title}"
    
class Comment(models.Model):
  user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
  place = models.ForeignKey(Place, on_delete=models.CASCADE)

  stroller_rental = models.BooleanField(default=False, verbose_name="유모차 대여")
  credit_card = models.BooleanField(default=False, verbose_name="신용카드 사용 가능")
  pet_friendly = models.BooleanField(default=False, verbose_name="애완동물 동반 가능")
  parking = models.BooleanField(default=False, verbose_name="주차 시설")
  restroom = models.BooleanField(default=False, verbose_name="화장실")
  elevator = models.BooleanField(default=False, verbose_name="엘리베이터")
  wheelchair_path = models.BooleanField(default=False, verbose_name="휠체어 통로")
  wheelchair_rental = models.BooleanField(default=False, verbose_name="휠체어 대여")

  content = models.TextField(verbose_name="내용")  # 댓글 내용
  created_at = models.DateTimeField(auto_now_add=True, verbose_name="작성일")  # 작성 시간
  updated_at = models.DateTimeField(auto_now=True, verbose_name="수정일")

  def __str__(self):
     return f'{self.user.nickname if self.user else '삭제된 사용자'}, {self.place}'
    
class Views(models.Model):
    place = models.ForeignKey('Place', on_delete=models.CASCADE)  # Place 모델과의 관계 설정
    count = models.PositiveIntegerField(default=0)  # 총 조회수
    users = models.ManyToManyField(User, related_name='viewed_places', blank=True)  # 조회한 사용자들

    def __str__(self):
        return f"{self.count}"