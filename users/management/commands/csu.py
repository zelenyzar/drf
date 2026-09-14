from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        email = "admin_pro@sky.pro"
        password = "123qwe"

        user, created = User.objects.update_or_create(
            email=email,
            defaults={
                "is_staff": True,
                "is_active": True,
                "is_superuser": True,
            },
        )
        user.set_password(password)
        user.save()

        if created:
            self.stdout.write(
                self.style.SUCCESS(f"Пользователь {email} успешно создан!")
            )
        else:
            self.stdout.write(
                self.style.WARNING(
                    f"Пользователь {email} уже существовал, права обновлены, пароль изменен."
                )
            )
