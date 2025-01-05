from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from transaction.models import Subscribe
from . import manager as self_manager
from django.db import models
from book.models import Book

AUTH_METHOD = (
    ("Credentials", "Credentials"),
    ("Google", "Google"),
    ("Github", "Github"),
)


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(
        max_length=1000,
        unique=True,
        primary_key=True,
        db_index=True,
    )
    email = models.EmailField(unique=True, max_length=254, blank=True, null=True)
    first_name = models.CharField(max_length=1000, blank=True)
    last_name = models.CharField(max_length=1000, blank=True)
    image = models.CharField(max_length=1000, blank=True, null=True)
    method = models.CharField(max_length=50, default="Credentials", choices=AUTH_METHOD)
    # password .....

    is_staff = models.BooleanField(default=True)
    is_active = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    groups = None
    user_permissions = None
    last_login = None

    objects = self_manager.UserManager()

    REQUIRED_FIELDS = ["first_name", "last_name", "email"]

    USERNAME_FIELD = "username"

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ["first_name"]

    def __str__(self) -> str:
        return self.username

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not Profile.objects.filter(user=self).exists():
            Profile.objects.create(user=self)
        return self

    def delete(self, *args, **kwargs):
        Profile.objects.get(user=self).delete()
        return super().delete(*args, **kwargs)


class LoginCode(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    uid = models.CharField(default="", max_length=4)
    token = models.CharField(default="", max_length=4)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Login Code"
        verbose_name_plural = "Login Codes"

    def __str__(self) -> str:
        return self.user.username


class ActivationCode(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    uid = models.CharField(default="", max_length=4)
    token = models.CharField(default="", max_length=4)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Activation Code"
        verbose_name_plural = "Activation Codes"

    def __str__(self) -> str:
        return self.user.username


class ResetPasswordCode(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    uid = models.CharField(default="", max_length=4)
    token = models.CharField(default="", max_length=4)

    class Meta:
        verbose_name = "Reset Password Code"
        verbose_name_plural = "Reset Password Codes"

    def __str__(self) -> str:
        return self.user.username


class ResetEmailCode(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    uid = models.CharField(default="", max_length=4)
    token = models.CharField(default="", max_length=4)
    new_email = models.EmailField(default="", max_length=254)

    class Meta:
        verbose_name = "Reset Email Code"
        verbose_name_plural = "Reset Email Codes"

    def __str__(self) -> str:
        return self.user.username


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    subscription = models.ForeignKey(
        Subscribe, on_delete=models.SET_NULL, null=True, blank=True
    )
    subscription_date = models.DateField(null=True, blank=True)
    penalty = models.BooleanField(default=False)
    penalty_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    week_borrow = models.PositiveIntegerField(default=0)
    month_borrow = models.PositiveIntegerField(default=0)
    year_borrow = models.PositiveIntegerField(default=0)
    holdings_no = models.PositiveIntegerField(default=0)
    holdings = models.ManyToManyField(Book, blank=True)
    pendings = models.ManyToManyField(Book, blank=True, related_name="pendings")

    def __str__(self):
        return f"{self.user.username}'s Profile"

    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"

    def __str__(self) -> str:
        return self.user.username
