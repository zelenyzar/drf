from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, RetrieveAPIView,
                                     UpdateAPIView)
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from materials.models import Course, Lesson
from materials.serializer import (CourseDetailSerializer, CourseSerializer,
                                  LessonSerializer)
from users.permissions import IsModer, IsOwner


class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all().prefetch_related("lessons")

    def get_serializer_class(self):
        if self.action == "retrieve":
            return CourseDetailSerializer
        return CourseSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = (~IsModer,)
        elif self.action in ["update", "retrieve"]:
            self.permission_classes = (IsModer | IsOwner,)
        elif self.action == "destroy":
            self.permission_classes = (~IsModer | IsOwner,)
        return super().get_permissions()


class LessonCreateApiView(CreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (~IsModer, IsAuthenticated)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonListApiView(ListAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    def get_queryset(self):
        course_id = self.request.query_params.get("course")
        if course_id:
            return Lesson.objects.filter(course_id=course_id)
        return Lesson.objects.all()


class LessonRetrieveApiView(RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated, IsModer | IsOwner)


class LessonUpdateApiView(UpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated, IsModer | IsOwner)


class LessonDestroyApiView(DestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated, IsOwner | ~IsModer)
