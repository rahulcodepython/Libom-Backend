from django.urls import path
from . import views

urlpatterns = [
    path("create/", views.BookCreateView.as_view(), name="book-create"),
    path("edit/<str:isbn_no>/", views.BookEditView.as_view(), name="book-edit"),
    path("book/<str:isbn_no>/", views.BookSingleView.as_view(), name="book-single"),
    path("list/", views.BookListView.as_view(), name="book-list"),
    path(
        "list/borrow/request/",
        views.BorrowRequestListView.as_view(),
        name="borrow-request-list",
    ),
    path(
        "borrow/request/<str:isbn_no>/",
        views.BorrowRequestView.as_view(),
        name="borrow-request",
    ),
    path(
        "borrow/approve/<str:id>/",
        views.BorrowApproveView.as_view(),
        name="borrow-approve",
    ),
    path(
        "borrow/reject/<str:id>/",
        views.BorrowRejectView.as_view(),
        name="borrow-reject",
    ),
    path(
        "list/return/request/",
        views.ReturnRequestListView.as_view(),
        name="return-request-list",
    ),
    path(
        "return/approve/<str:id>/",
        views.ReturnApproveView.as_view(),
        name="return-approve",
    ),
    path(
        "list/borrowed/",
        views.BorrowedBookListView.as_view(),
        name="borrowed-book-list",
    ),
]
