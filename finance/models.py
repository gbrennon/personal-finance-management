# finance/models.py
from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal


# --- NEW CATEGORY MODEL ---
# This model will store all your custom income and expense categories in the database.
class Category(models.Model):
    TRANSACTION_TYPES = [
        ("Income", "Income"),
        ("Expense", "Expense"),
    ]

    # Each category belongs to a specific user
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # The name of the category (e.g., "Salary", "Rent")
    name = models.CharField(max_length=100)
    # The type of the category, either 'Income' or 'Expense'
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)

    def __str__(self):
        return self.name

    class Meta:
        # Ensures a user cannot have two categories with the same name and type
        unique_together = ("user", "name", "transaction_type")
        verbose_name_plural = "Categories"


# --- UPDATED TRANSACTION MODEL ---
class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ("Income", "Income"),
        ("Expense", "Expense"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    # The 'category' field is now a relationship to the Category model
    category = models.ForeignKey(Category, on_delete=models.PROTECT)

    date = models.DateField()

    # The old 'type' field is removed as it's redundant.

    def __str__(self):
        return f"{self.get_transaction_type_display()} - {self.category.name} - {self.amount}"


class Budget(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    month = models.IntegerField()
    year = models.IntegerField()

    def __str__(self):
        return f"{self.user.username} - {self.month}/{self.year}: {self.amount or 'Not Set'}"

    class Meta:
        unique_together = ("user", "month", "year")


class RetirementGoal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    target_amount = models.DecimalField(max_digits=15, decimal_places=2)
    target_date = models.DateField()
    current_amount = models.DecimalField(
        max_digits=15, decimal_places=2, default=Decimal("0")
    )
    monthly_contribution = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - Retirement Goal: {self.target_amount}"

    @property
    def progress_percentage(self):
        if self.target_amount > 0:
            return (self.current_amount / self.target_amount) * 100
        return 0


class RetirementContribution(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    retirement_goal = models.ForeignKey(RetirementGoal, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    contribution_date = models.DateField()
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - Contribution: {self.amount} on {self.contribution_date}"

    class Meta:
        ordering = ["-contribution_date"]


class CryptoInvestment(models.Model):
    CRYPTO_CHOICES = [
        ("BTC", "Bitcoin"),
        ("ETH", "Ethereum"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    crypto_type = models.CharField(max_length=3, choices=CRYPTO_CHOICES)
    amount_invested = models.DecimalField(max_digits=15, decimal_places=2)
    quantity = models.DecimalField(max_digits=20, decimal_places=8)
    purchase_price = models.DecimalField(max_digits=15, decimal_places=2)
    purchase_date = models.DateField()
    current_price = models.DecimalField(
        max_digits=15, decimal_places=2, null=True, blank=True
    )

    def __str__(self):
        return f"{self.user.username} - {self.crypto_type}: {self.quantity}"

    @property
    def current_value(self):
        if self.current_price:
            return self.quantity * self.current_price
        return None

    @property
    def profit_loss(self):
        if self.current_value:
            return self.current_value - self.amount_invested
        return None

    @property
    def profit_loss_percentage(self):
        if self.current_value and self.amount_invested > 0:
            return (
                (self.current_value - self.amount_invested) / self.amount_invested
            ) * 100
        return None

    class Meta:
        ordering = ["-purchase_date"]
