from rest_framework.serializers import ModelSerializer, SerializerMethodField

from materials.models import Course, Lesson


class CourseSerializer(ModelSerializer):
    lessons_count = SerializerMethodField()

    class Meta:
        model = Course
        fields = "__all__"

    def get_lessons_count(self, obj):
        return obj.lessons.count()


class CourseDetailSerializer(ModelSerializer):
    lessons_count = SerializerMethodField()

    class Meta:
        model = Course
        fields = ('title', 'description', 'lessons_count')

    def get_lessons_count(self, obj):
        return obj.lessons.count()




class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"
