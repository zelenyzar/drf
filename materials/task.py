import logging
import os

from celery import shared_task
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from dotenv import load_dotenv

from materials.models import Course

load_dotenv(override=True)

logger = logging.getLogger(__name__)


@shared_task(max_retries=3)
def mailing(email: str, course_id: int):
    try:
        course = Course.objects.get(id=course_id)
    except Course.DoesNotExist:
        logger.error(
            f"Курс с ID={course_id} не найден, пропускаем рассылку для {email}"
        )
        return

    host = os.getenv("HOST")
    if not host:
        logger.error("Переменная окружения HOST не задана")
        # Можно сделать retry, если хочешь, но для простоты просто выходим
        return

    url = f"{host}/materials/{course_id}"
    logger.info(f"Отправка письма на {email}")

    subject = f"Обновление курса «{course.title}»"
    message_text = (
        f"Курс «{course.title}» был обновлён.\n\n"
        f"Перейдите по ссылке, чтобы увидеть изменения: {url}"
    )

    try:
        send_mail(
            subject=subject,
            message=message_text,
            from_email=os.getenv("EMAIL_HOST_USER"),
            recipient_list=[email],
        )
        logger.info(f"Письмо успешно отправлено на {email}")
    except Exception as exc:
        logger.exception(f"Ошибка отправки на {email}: {exc}")
    # send_mail(
    #     subject= f"Обновление курса {course.title}",
    #     message= f"Обновлен курс {course.title}. Для того, чтобы увидеть изменения перейдите по ссылке: {url} ",
    #     from_email=os.getenv("EMAIL_HOST_USER"),
    #     recipient_list=email,
    # )
    # logger.info(f"✅ Письмо отправлено на {email}")
