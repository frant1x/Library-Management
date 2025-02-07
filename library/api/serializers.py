from rest_framework import serializers
from authentication.models import CustomUser
from order.models import Order
from author.models import Author
from book.models import Book
from django.contrib.auth.hashers import make_password


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            "id",
            "first_name",
            "last_name",
            "middle_name",
            "email",
            "password",
            "created_at",
            "updated_at",
            "role",
        ]

    def create(self, validated_data):
        validated_data["password"] = make_password(validated_data["password"])
        user = super(UserSerializer, self).create(validated_data)
        user.is_active = True
        if user.role == 1:
            user.is_superuser = True
            user.is_staff = True
        else:
            user.is_superuser = False
            user.is_staff = False
        user.save()
        return user

    def update(self, instance, validated_data):
        validated_data["password"] = make_password(validated_data["password"])
        user = super().update(instance, validated_data)
        if user.role == 1:
            user.is_superuser = True
            user.is_staff = True
        else:
            user.is_superuser = False
            user.is_staff = False
        user.save()
        return user


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = "__all__"

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'
