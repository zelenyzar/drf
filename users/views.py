from django_filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, viewsets
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import AllowAny

from users.filters import PaymentFilter
from users.models import Payment, User
from users.serializers import PaymentSerializer, UserSerializer


class UserCreateAPIView(CreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class UserPaymentsListAPIView(ListAPIView):
    serializer_class = PaymentSerializer

    def get_queryset(self):
        user_id = self.kwargs.get("user_id")
        return Payment.objects.filter(user_id=user_id)


class PaymentViewSet(viewsets.ModelViewSet):
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]

    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = PaymentFilter
    ordering_fields = ["paid_at"]
    ordering = ["-paid_at"]

    def get_queryset(self):
        return Payment.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
