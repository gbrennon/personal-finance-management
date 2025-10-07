from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from django.db.models import Sum
from django.db.models.functions import TruncMonth
from datetime import datetime, timedelta
from .models import Category, Transaction, Budget
from .serializers import (
    CategorySerializer,
    TransactionSerializer,
    BudgetSerializer,
    UserSerializer,
)


class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TransactionViewSet(viewsets.ModelViewSet):
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user).order_by("-date")

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=["get"])
    def summary(self, request):
        """Get financial summary for the user"""
        transactions = self.get_queryset()

        total_income = (
            transactions.filter(transaction_type="Income").aggregate(
                total=Sum("amount")
            )["total"]
            or 0
        )
        total_expense = (
            transactions.filter(transaction_type="Expense").aggregate(
                total=Sum("amount")
            )["total"]
            or 0
        )
        total_savings = abs(total_income - total_expense)

        return Response(
            {
                "total_income": total_income,
                "total_expense": total_expense,
                "total_savings": total_savings,
            }
        )

    @action(detail=False, methods=["get"])
    def monthly_report(self, request):
        """Get monthly financial report"""
        transactions = (
            self.get_queryset()
            .annotate(month=TruncMonth("date"))
            .values("month", "transaction_type")
            .annotate(total=Sum("amount"))
            .order_by("month")
        )

        monthly_data = {}
        for transaction in transactions:
            month_key = transaction["month"].strftime("%Y-%m")
            if month_key not in monthly_data:
                monthly_data[month_key] = {"Income": 0, "Expense": 0}
            monthly_data[month_key][transaction["transaction_type"]] = float(
                transaction["total"]
            )

        return Response(monthly_data)


class BudgetViewSet(viewsets.ModelViewSet):
    serializer_class = BudgetSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Budget.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=["get"])
    def current_month(self, request):
        """Get budget for current month"""
        now = datetime.now()
        try:
            budget = Budget.objects.get(
                user=request.user, month=now.month, year=now.year
            )
            serializer = self.get_serializer(budget)
            return Response(serializer.data)
        except Budget.DoesNotExist:
            return Response(
                {"detail": "No budget set for current month"},
                status=status.HTTP_404_NOT_FOUND,
            )
