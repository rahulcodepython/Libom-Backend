from rest_framework.views import APIView
from rest_framework import permissions, response
from .serializers import (
    CreateBookSerializer,
    EditBookSerializer,
    BookSingleSerializer,
    BookListSerializer,
    BorrowingSerializer,
    ReturningSerializer,
)
from backend.decorators import catch_exception
from backend.message import Message
from django.shortcuts import get_object_or_404
from .models import Book, Borrowing, Returning
from datetime import date
import uuid
from authentication.models import Profile
from datetime import timedelta

today = date.today()


class BookCreateView(APIView):
    permission_classes = [permissions.IsAdminUser]

    @catch_exception
    def post(self, request, *args, **kwargs):
        serializer = CreateBookSerializer(data=request.data)
        if not serializer.is_valid():
            return Message.error("Invalid data.")
        serializer.save()
        return Message.create("Book is added.")


class BookEditView(APIView):
    permission_classes = [permissions.IsAdminUser]

    @catch_exception
    def patch(self, request, isbn_no, *args, **kwargs):
        book_instance = get_object_or_404(Book, isbn_no=isbn_no)
        serializer = EditBookSerializer(book_instance, data=request.data, partial=True)
        if not serializer.is_valid():
            return Message.error("Invalid data.")
        serializer.save()
        return Message.create("Book is updated.")


class BookSingleView(APIView):
    permission_classes = [permissions.IsAdminUser]

    @catch_exception
    def get(self, request, isbn_no, *args, **kwargs):
        book_instance = get_object_or_404(Book, isbn_no=isbn_no)
        serializer = BookSingleSerializer(book_instance)
        return response.Response(serializer.data)


class BookListView(APIView):
    permission_classes = [permissions.AllowAny]

    @catch_exception
    def get(self, request, *args, **kwargs):
        books = Book.objects.all()
        print(books)
        serializer = BookListSerializer(books, many=True, context={"request": request})
        return response.Response(serializer.data)


class BorrowRequestView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @catch_exception
    def get(self, request, isbn_no, *args, **kwargs):
        profile = Profile.objects.get(user=request.user)
        plan = profile.subscription

        if profile.holdings_no >= plan.max_borrow:
            return Message.error("You have reached the maximum borrow limit.")

        if (profile.subscription_date + timedelta(days=plan.duration)) < today:
            return Message.error("Your subscription has expired.")

        book = get_object_or_404(Book, isbn_no=isbn_no)
        Borrowing.objects.create(
            isbn_no=book.isbn_no, user=request.user, id=f"{today}-{uuid.uuid4()}"
        )
        profile = Profile.objects.get(user=request.user)
        profile.pendings.add(book)
        return Message.create("Borrow request is created.")


class BorrowRequestListView(APIView):
    permission_classes = [permissions.IsAdminUser]

    @catch_exception
    def get(self, request, *args, **kwargs):
        borrowings = Borrowing.objects.all()
        serializer = BorrowingSerializer(borrowings, many=True)
        return response.Response(serializer.data)


class BorrowApproveView(APIView):
    permission_classes = [permissions.IsAdminUser]

    @catch_exception
    def post(self, request, id, *args, **kwargs):
        borrowing = get_object_or_404(Borrowing, id=id)
        book = get_object_or_404(Book, isbn_no=borrowing.isbn_no)
        profile = Profile.objects.get(user=borrowing.user)

        if book.quantity < 1:
            return Message.error("Book is out of stock.")

        book.quantity -= 1
        book.save()

        profile.pendings.remove(book)
        profile.holdings.add(book)
        profile.holdings_no += 1
        profile.save()

        borrowing.state = "approved"
        borrowing.save()

        Returning.objects.create(
            isbn_no=borrowing.isbn_no,
            user=borrowing.user,
            id=f"{today}-{uuid.uuid4()}",
            borrow_date=borrowing.date,
        )

        return Message.success("Borrow request is approved.")


class BorrowRejectView(APIView):
    permission_classes = [permissions.IsAdminUser]

    @catch_exception
    def post(self, request, id, *args, **kwargs):
        borrowing = get_object_or_404(Borrowing, id=id)
        borrowing.state = "cancel"
        borrowing.save()
        return Message.success("Borrow request is rejected.")


class ReturnRequestListView(APIView):
    permission_classes = [permissions.IsAdminUser]

    @catch_exception
    def get(self, request, *args, **kwargs):
        returnings = Returning.objects.all()
        serializer = ReturningSerializer(returnings, many=True)
        return response.Response(serializer.data)


class ReturnApproveView(APIView):
    permission_classes = [permissions.IsAdminUser]

    @catch_exception
    def post(self, request, id, *args, **kwargs):
        returning = get_object_or_404(Returning, id=id)
        book = get_object_or_404(Book, isbn_no=returning.isbn_no)
        profile = Profile.objects.get(user=returning.user)

        book.quantity += 1
        book.save()

        profile.holdings.remove(book)
        profile.holdings_no -= 1
        profile.save()

        returning.state = "approved"
        returning.return_date = today
        returning.save()

        return Message.success("Borrow request is approved.")
