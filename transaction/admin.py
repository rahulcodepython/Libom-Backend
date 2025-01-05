from django.contrib import admin
from . import models


@admin.register(models.Subscribe)
class SubscribeAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "amount",
        "max_borrow",
        "journal_access",
        "premium_book_access",
        "holding_time",
        "duration",
    ]


@admin.register(models.Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "amount", "date", "type", "mode"]
