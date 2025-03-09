from django.db import models


class Book(models.Model):
    isbn_no = models.CharField(max_length=13, unique=True, primary_key=True)
    name = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField()
    category = models.CharField(max_length=100)
    image = models.URLField(max_length=500, blank=True)

    def __str__(self):
        return self.name


STATE_CHOICES = [
    ("approved", "Approved"),
    ("cancel", "Cancel"),
    ("pending", "Pending"),
]


class Borrowing(models.Model):
    id = models.CharField(primary_key=True, unique=True, max_length=1000)
    isbn_no = models.CharField(max_length=13)
    user = models.ForeignKey("authentication.User", on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    state = models.CharField(max_length=10, choices=STATE_CHOICES, default="pending")

    def __str__(self):
        return f"Borrowing {self.id} by {self.user.username}"


class Returning(models.Model):
    id = models.CharField(primary_key=True, unique=True, max_length=1000)
    isbn_no = models.CharField(max_length=13)
    user = models.ForeignKey("authentication.User", on_delete=models.CASCADE)
    borrow_date = models.DateField()
    return_date = models.DateField(null=True, blank=True)
    state = models.CharField(max_length=10, choices=STATE_CHOICES, default="pending")

    def __str__(self):
        return f"Returning {self.id} by {self.user.username}"
