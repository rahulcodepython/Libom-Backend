from django.urls import path
from . import views

urlpatterns = [
    path("subscription/", views.SubscriptionView.as_view(), name="subscription"),
    path("subscribe/<str:id>/", views.SubscribeView.as_view(), name="subscribe"),
]
