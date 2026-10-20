from celery import shared_task
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
import logging

logger = logging.getLogger(__name__)

@shared_task
def deactivate_inactive_users():
    """
    Блокирует пользователей, которые не заходили более 30 дней.
    Использует AUTH_USER_MODEL, чтобы корректно работать с кастомной моделью.
    """
    User = settings.AUTH_USER_MODEL
    from django.apps import apps
    UserModel = apps.get_model(User)

    now = timezone.now()
    one_month_ago = now - timedelta(days=30)

    inactive_users = UserModel.objects.filter(
        last_login__lt=one_month_ago,
        is_active=True,
    )

    count = inactive_users.count()
    if count == 0:
        logger.info("Нет неактивных пользователей для блокировки.")
        return

    logger.info(f"Блокируем {count} неактивных пользователей.")

    updated = inactive_users.update(is_active=False)
    logger.info(f"Обновлено записей: {updated}")
