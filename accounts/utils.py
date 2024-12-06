from django.core.mail import send_mail
from django.conf import settings

def send_verification_email(email, verification_code):
    """
    인증 코드를 이메일로 전송
    """
    subject = '[Tour4Int] 이메일 인증 코드'
    message = f'''안녕하세요!
    
회원가입을 위한 이메일 인증 코드입니다:

{verification_code}

이 코드는 30분 동안만 유효합니다.
코드를 입력하여 이메일 인증을 완료해주세요.

감사합니다.
Tour4Int 팀'''
    
    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email],
        fail_silently=False,
    )
