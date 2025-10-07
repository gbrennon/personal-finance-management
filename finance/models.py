# finance/models.py
from django.db import models
from django.contrib.auth.models import User


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


# --- NEW INVOICE MODEL ---
class Invoice(models.Model):
    STATUS_CHOICES = [
        ("draft", "Draft"),
        ("sent", "Sent"),
        ("paid", "Paid"),
        ("overdue", "Overdue"),
        ("cancelled", "Cancelled"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    invoice_number = models.CharField(max_length=50, unique=True)
    client_name = models.CharField(max_length=200)
    client_email = models.EmailField(blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)
    issue_date = models.DateField(auto_now_add=True)
    due_date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="draft")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Invoice {self.invoice_number} - {self.client_name} - ${self.amount}"

    class Meta:
        ordering = ["-created_at"]


# --- NEW INVESTMENT MODEL ---
class Investment(models.Model):
    INVESTMENT_TYPES = [
        ("stocks", "Stocks"),
        ("bonds", "Bonds"),
        ("mutual_funds", "Mutual Funds"),
        ("etf", "ETF"),
        ("real_estate", "Real Estate"),
        ("crypto", "Cryptocurrency"),
        ("commodities", "Commodities"),
        ("other", "Other"),
    ]

    RISK_LEVELS = [
        ("low", "Low Risk"),
        ("medium", "Medium Risk"),
        ("high", "High Risk"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    investment_type = models.CharField(max_length=20, choices=INVESTMENT_TYPES)
    amount_invested = models.DecimalField(max_digits=12, decimal_places=2)
    current_value = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True
    )
    expected_return_rate = models.DecimalField(
        max_digits=5, decimal_places=2, help_text="Expected annual return rate (%)"
    )
    risk_level = models.CharField(max_length=10, choices=RISK_LEVELS, default="medium")
    purchase_date = models.DateField()
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.get_investment_type_display()} - ${self.amount_invested}"

    @property
    def current_return(self):
        if self.current_value:
            return self.current_value - self.amount_invested
        return 0

    @property
    def return_percentage(self):
        if self.current_value and self.amount_invested > 0:
            return (
                (self.current_value - self.amount_invested) / self.amount_invested
            ) * 100
        return 0

    class Meta:
        ordering = ["-created_at"]


# --- NEW RETIREMENT PLAN MODEL ---
class RetirementPlan(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    target_retirement_amount = models.DecimalField(max_digits=12, decimal_places=2)
    current_age = models.IntegerField()
    target_retirement_age = models.IntegerField()
    monthly_contribution = models.DecimalField(max_digits=10, decimal_places=2)
    current_savings = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    expected_annual_return = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=7.0,
        help_text="Expected annual return rate (%)",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Retirement Plan - Target: ${self.target_retirement_amount}"

    @property
    def years_to_retirement(self):
        return self.target_retirement_age - self.current_age

    @property
    def months_to_retirement(self):
        return self.years_to_retirement * 12

    def calculate_projected_amount(self):
        """Calculate projected retirement amount based on current savings and monthly contributions"""
        if self.years_to_retirement <= 0:
            return self.current_savings

        monthly_rate = (self.expected_annual_return / 100) / 12
        months = self.months_to_retirement

        # Future value of current savings
        future_current = float(self.current_savings) * ((1 + monthly_rate) ** months)

        # Future value of monthly contributions (annuity)
        if monthly_rate > 0:
            future_contributions = float(self.monthly_contribution) * (
                ((1 + monthly_rate) ** months - 1) / monthly_rate
            )
        else:
            future_contributions = float(self.monthly_contribution) * months

        return future_current + future_contributions

    def is_on_track(self):
        """Check if current plan will meet retirement goal"""
        projected = self.calculate_projected_amount()
        return projected >= float(self.target_retirement_amount)

    class Meta:
        verbose_name = "Retirement Plan"
        verbose_name_plural = "Retirement Plans"
