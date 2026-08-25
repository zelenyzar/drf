from django_filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions
from rest_framework.generics import ListAPIView

from users.filters import PaymentFilter
from users.models import Payment
from users.serializers import PaymentSerializer

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