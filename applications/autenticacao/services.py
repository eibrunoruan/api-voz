import random
from django.utils import timezone
from datetime import timedelta
from django.core.mail import send_mail
from django.conf import settings

def generate_verification_code():
    """Gera um código numérico aleatório de 5 dígitos."""
    return str(random.randint(10000, 99999))

def send_verification_email(user, subject, message_template):
    """
    Gera um código, salva no usuário e envia o e-mail.
    """
    code = generate_verification_code()
    
    # Define o tempo de expiração do código (ex: 15 minutos)
    user.verification_code = code
    user.code_expires_at = timezone.now() + timedelta(minutes=15)
    user.save()

    # Envia o e-mail
    message = message_template.format(code=code)
    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        fail_silently=False,
    )
    return code
