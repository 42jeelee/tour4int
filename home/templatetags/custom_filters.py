from django import template
from django.utils import timezone
from datetime import timedelta, datetime

register = template.Library()

@register.filter
def is_close_deadline(value, days):
  if value and isinstance(value, datetime):
    today = timezone.now()

    diff = value - today

    return diff.days <= days

  return False

@register.filter
def get_diffday(value):
  if value and isinstance(value, datetime):
    today = timezone.now()

    diff = value - today

    return diff.days

  return 0

@register.filter
def custom_date(value):
  if value and isinstance(value, datetime):
    weeks = ['일', '월', '화', '수', '목', '금', '토']
    
    return value.strftime(f"%Y년 %m월 %d일 ({weeks[value.weekday()]})")
  return value



