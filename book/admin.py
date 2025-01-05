from django.contrib import admin
from . import models


@admin.register(models.Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ["isbn_no", "name", "author", "quantity", "category"]


@admin.register(models.Borrowing)
class BorrowingAdmin(admin.ModelAdmin):
    list_display = ["id", "isbn_no", "user", "date", "state"]


@admin.register(models.Returning)
class ReturningAdmin(admin.ModelAdmin):
    list_display = ["id", "isbn_no", "user", "borrow_date", "return_date", "state"]
