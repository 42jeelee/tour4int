from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import ApiFetchLog

@receiver(post_migrate)
def init_ApiFetchLog(sender, **kwargs):
  if not ApiFetchLog.objects.exists():
    ApiFetchLog.objects.create()

    print("✔ Initial ApiFetchLog")