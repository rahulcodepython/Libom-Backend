from django.db import models
from datetime import date
import uuid

today = date.today()


class Subscribe(models.Model):
    id = models.CharField(primary_key=True, unique=True, max_length=100)
    amount = models.PositiveIntegerField()
    max_borrow = models.PositiveIntegerField()
    subscriber = models.ManyToManyField("authentication.User", blank=True)
    journal_access = models.BooleanField(default=False)
    premium_book_access = models.BooleanField(default=False)
    holding_time = models.PositiveIntegerField()
    duration = models.PositiveIntegerField(choices=[(30, "Monthly"), (365, "Yearly")])
    subscriber = models.ManyToManyField("authentication.User", blank=True)

    def __str__(self):
        return f"Subscription {self.id}"


class Transaction(models.Model):
    TYPE_CHOICES = [
        ("penalty", "Penalty"),
        ("subscribe", "Subscribe"),
    ]

    MODE_CHOICES = [
        ("online", "Online"),
    ]

    id = models.CharField(primary_key=True, unique=True, max_length=1000)
    user = models.ForeignKey("authentication.User", on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(auto_now_add=True)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    mode = models.CharField(max_length=10, choices=MODE_CHOICES)

    def __str__(self):
        return f"Transaction {self.id} for {self.user.username} ({self.type})"

    def save(self, *args, **kwargs):
        if not id:
            self.id = today + uuid.uuid4()

        return super().save(*args, **kwargs)
