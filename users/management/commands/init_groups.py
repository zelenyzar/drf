from django.core.management import BaseCommand
from django.contrib.auth.models import Group


class Command(BaseCommand):
    help = 'Создает группу модераторов "moders", если её нет'

    def handle(self, *args, **options):
        group_name = "moders"

        # get_or_create возвращает кортеж: (объект, создан_ли_он)
        group, created = Group.objects.get_or_create(name=group_name)

        if created:
            self.stdout.write(self.style.SUCCESS(f'Группа "{group_name}" успешно создана!'))
        else:
            self.stdout.write(self.style.WARNING(f'Группа "{group_name}" уже существует.'))
