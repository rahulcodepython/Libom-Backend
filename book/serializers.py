from rest_framework import serializers
from .models import Book


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
