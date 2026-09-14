from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError
from django.utils.crypto import get_random_string

User = get_user_model()


class Command(BaseCommand):
    help = "Создаёт тестового пользователя для разработки."

    def add_arguments(self, parser):
        parser.add_argument(
            "--email", type=str, required=False, help="Email пользователя"
        )
        parser.add_argument("--password", type=str, default="test1234", help="Пароль")
        parser.add_argument(
            "--is-staff", action="store_true", help="Staff-пользователь"
        )
        parser.add_argument(
            "--is-superuser", action="store_true", help="Суперпользователь"
        )

    def handle(self, *args, **options):
        email = options["email"] or f"test-{get_random_string(8)}@example.com"
        password = options["password"]
        is_staff = options["is_staff"]
        is_superuser = options.get("is_superuser", False)

        if User.objects.filter(email=email).exists():
            raise CommandError(f"Пользователь с email {email} уже существует.")

        if is_superuser:
            user = User.objects.create_superuser(email=email, password=password)
            self.stdout.write(self.style.SUCCESS(f"Суперпользователь: {email}"))
        elif is_staff:
            user = User.objects.create_user(
                email=email, password=password, is_staff=True
            )
            self.stdout.write(self.style.SUCCESS(f"Staff: {email}"))
        else:
            user = User.objects.create_user(email=email, password=password)
            self.stdout.write(self.style.SUCCESS(f"Пользователь: {email}"))

        self.stdout.write(f"Пароль: {password}")
