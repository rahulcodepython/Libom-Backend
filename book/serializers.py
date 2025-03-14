from rest_framework import serializers
from .models import Book, Borrowing, Returning
from authentication.models import Profile


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book


class CreateBookSerializer(BookSerializer):
    class Meta(BookSerializer.Meta):
        fields = "__all__"

    def create(self, validated_data):
        return Book.objects.create(**validated_data)


class EditBookSerializer(BookSerializer):
    class Meta(BookSerializer.Meta):
        exclude = ["isbn_no"]

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)


class BookSingleSerializer(BookSerializer):
    class Meta(BookSerializer.Meta):
        fields = "__all__"


class BookListSerializer(BookSerializer):
    borrowed = serializers.SerializerMethodField()
    request_pending = serializers.SerializerMethodField()

    class Meta(BookSerializer.Meta):
        fields = "__all__"

    def get_borrowed(self, obj):
        user = self.context["request"].user
        if user.is_anonymous:
            return False

        profile = Profile.objects.get(user=user)
        return profile.holdings.filter(isbn_no=obj.isbn_no).exists()

    def get_request_pending(self, obj):
        user = self.context["request"].user
        if user.is_anonymous:
            return False

        profile = Profile.objects.get(user=user)
        return profile.pendings.filter(isbn_no=obj.isbn_no).exists()


class BorrowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = "__all__"


class ReturningSerializer(serializers.ModelSerializer):
    class Meta:
        model = Returning
        fields = "__all__"
