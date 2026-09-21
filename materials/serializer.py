from django.template.context_processors import request
from pyexpat.errors import messages
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, SerializerMethodField

from materials.models import Course, Lesson, Subscription
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

    def get_subscription(self, obj):
        message = 'Подписка отсутствует'
        request = self.context.get("request")
        if request:
            subscriptions = Subscription.objects.filter(user=request.user)
            for subscription in subscriptions:
                if subscription.course == obj:
                    message = 'Вы подписаны на этот курс'
        return message


class SubscriptionSerializer(ModelSerializer):
    course = CourseSerializer(read_only=True)

    class Meta:
        model = Subscription
        fields = "__all__"
        read_only_fields = ("user", "course")