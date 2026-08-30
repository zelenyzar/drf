from django.conf import settings
from django.db import migrations

def populate_owners(apps, schema_editor):
    Course = apps.get_model('materials', 'Course')
    Lesson = apps.get_model('materials', 'Lesson')
    User = apps.get_model(*settings.AUTH_USER_MODEL.split('.', 1))

    default_user = User.objects.first()
    if not default_user:
        return

    Course.objects.filter(owner__isnull=True).update(owner=default_user)

    Lesson.objects.filter(owner__isnull=True).update(owner=default_user)


def reverse_populate_owners(apps, schema_editor):
    Course = apps.get_model('materials', 'Course')
    Lesson = apps.get_model('materials', 'Lesson')

    Course.objects.update(owner=None)
    Lesson.objects.update(owner=None)


class Migration(migrations.Migration):
    dependencies = [
        ('materials', '0002_course_owner_lesson_owner'),
    ]

    operations = [
        migrations.RunPython(populate_owners, reverse_populate_owners),
    ]
