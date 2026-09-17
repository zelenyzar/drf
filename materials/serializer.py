from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, SerializerMethodField

from materials.models import Course, Lesson
from materials.validators import url_validator


class LessonSerializer(ModelSerializer):
    video_url = serializers.URLField(validators=[url_validator])
    class Meta:
        model = Lesson
        fields = "__all__"


class CourseSerializer(ModelSerializer):
    lessons_count = SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = "__all__"

    def get_lessons_count(self, obj):
        return obj.lessons.count()


class CourseDetailSerializer(ModelSerializer):
    lessons_count = SerializerMethodField()

    class Meta:
        model = Course
        fields = ("title", "description", "lessons_count")

    def get_lessons_count(self, obj):
        return obj.lessons.count()
