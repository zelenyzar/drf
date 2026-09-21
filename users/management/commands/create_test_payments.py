import random
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.management import BaseCommand

from materials.models import Course, Lesson
from users.models import Payment

User = get_user_model()


class Command(BaseCommand):
    help = "Create test payments"

    def handle(self, *args, **options):
        users = list(User.objects.all())
        if not users:
            self.stdout.write("Нет пользователей. Создайте хотя бы одного.")
            return

        courses = list(Course.objects.all())
        lessons = list(Lesson.objects.all())

        if not courses and not lessons:
            self.stdout.write("Нет курсов и уроков. Сначала создайте их.")
            return

        methods = ["cash", "transfer"]

        for i in range(5):
            user = random.choice(users)
            method = random.choice(methods)
            amount = (
                Decimal(random.randint(300, 5000))
                + Decimal(random.randint(0, 99)) / 100
            )

            if courses and random.choice([True, False]):
                paid_course = random.choice(courses)
                paid_lesson = None
            elif lessons:
                paid_course = None
                paid_lesson = random.choice(lessons)
            else:
                self.stdout.write(f"Пропущен платёж #{i + 1}: нет курсов или уроков")
                continue

            payment, created = Payment.objects.get_or_create(
                user=user,
                paid_course=paid_course,
                paid_lesson=paid_lesson,
                amount=amount,
                payment_method=method,
            )

            if created:
                self.stdout.write(self.style.SUCCESS(f"Создан платёж #{payment.id}"))
            else:
                self.stdout.write(
                    self.style.WARNING(
                        f"Платёж уже существует (user={user.id}, course={paid_course.id if paid_course else None}, lesson={paid_lesson.id if paid_lesson else None})"
                    )
                )

        self.stdout.write(self.style.SUCCESS("Готово."))
