from celery import shared_task
import time
from django.core.mail import send_mail


@shared_task
def add(x, y):
    time.sleep(3)
    return x + y

#
@shared_task
def periodic_task():
    print("Эта задача запустилась по расписанию!")


@shared_task
def send_welcome_email(to_email):
    subject = "Добро пожаловать!"
    message = "Спасибо за регистрацию на нашем сайте."
    from_email = None 
    recipient_list = [to_email]

    send_mail(subject, message, from_email, recipient_list)
    return f"Письмо отправлено на {to_email}"
