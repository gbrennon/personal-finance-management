from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Category, Transaction, Budget


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name"]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "transaction_type", "user"]
        read_only_fields = ["user"]


class TransactionSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source="category.name", read_only=True)

    class Meta:
        model = Transaction
        fields = [
            "id",
            "transaction_type",
            "amount",
            "category",
            "category_name",
            "date",
            "user",
        ]
        read_only_fields = ["user"]


class BudgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Budget
        fields = ["id", "amount", "month", "year", "user"]
        read_only_fields = ["user"]
