from rest_framework.views import APIView
from rest_framework import permissions, response
from .serializers import CreateBookSerializer, EditBookSerializer, BookSingleSerializer
from backend.decorators import catch_exception
from backend.message import Message
from django.shortcuts import get_object_or_404
from .models import Book


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
