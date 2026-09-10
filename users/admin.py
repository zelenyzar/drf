from django.contrib import admin
from .models import Payment, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_filter = ('id', 'email')


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "paid_course",
        "paid_lesson",
        "amount",
        "payment_method",
        "paid_at",
    )

    list_filter = (
        "payment_method",
        ("paid_at", admin.DateFieldListFilter),
    )

    search_fields = (
        "user__email",
        "paid_course__title",
        "paid_lesson__title",
    )

    ordering = ("-paid_at",)

    fieldsets = (
        ("Основная информация", {
            "fields": ("user", "amount", "payment_method"),
        }),
        ("Детали оплаты", {
            "fields": ("paid_course", "paid_lesson"),
        }),
        ("Дата и время", {
            "fields": ("paid_at",),
        }),
    )
