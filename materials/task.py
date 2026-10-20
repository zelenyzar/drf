from celery import shared_task
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from materials.models import Course
import logging

from dotenv import load_dotenv
import os

load_dotenv(override=True)

logger = logging.getLogger(__name__)


@shared_task
def mailing(email, course_id):
    course = get_object_or_404(Course, id=course_id)
    host = os.getenv("HOST")
    url = f"{host}/materials/{course_id}"
    logger.info(f"📧 Отправка письма на {email}")
    send_mail(
        subject= f"Обновление курса {course.title}",
        message= f"Обновлен курс {course.title}. Для того, чтобы увидеть изменения перейдите по ссылке: {url} ",
        from_email=os.getenv("EMAIL_HOST_USER"),
        recipient_list=email,
    )
    logger.info(f"✅ Письмо отправлено на {email}")