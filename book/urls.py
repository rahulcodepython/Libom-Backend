from django.urls import path
from . import views

urlpatterns = [
    path("create/", views.BookCreateView.as_view(), name="book-create"),
    path("edit/<str:isbn_no>/", views.BookEditView.as_view(), name="book-edit"),
    path("<str:isbn_no>/", views.BookSingleView.as_view(), name="book-single"),
]
