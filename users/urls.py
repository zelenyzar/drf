from django.urls import path
from users.views import UserPaymentsListAPIView

urlpatterns = [
    path("payments/user/<int:user_id>/", UserPaymentsListAPIView.as_view(), name="user-payments"),
]
