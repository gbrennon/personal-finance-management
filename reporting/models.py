from django.db import models
from django.contrib.auth.models import User


class FinancialReport(models.Model):
    REPORT_TYPES = [
        ("monthly_summary", "Monthly Summary"),
        ("yearly_summary", "Yearly Summary"),
        ("budget_analysis", "Budget Analysis"),
        ("spending_trends", "Spending Trends"),
    ]

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("processing", "Processing"),
        ("completed", "Completed"),
        ("failed", "Failed"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    report_type = models.CharField(max_length=50, choices=REPORT_TYPES)
    title = models.CharField(max_length=200)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    report_data = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    # Report parameters
    month = models.IntegerField(null=True, blank=True)
    year = models.IntegerField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title} - {self.user.username}"


class ReportMetrics(models.Model):
    """
    Aggregated metrics for reporting.
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    month = models.IntegerField()
    year = models.IntegerField()

    total_income = models.DecimalField(max_digits=12, decimal_places=2, default="0.00")
    total_expenses = models.DecimalField(
        max_digits=12, decimal_places=2, default="0.00"
    )
    total_savings = models.DecimalField(max_digits=12, decimal_places=2, default="0.00")
    budget_amount = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True
    )
    budget_utilization = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True
    )  # Percentage

    transaction_count = models.IntegerField(default=0)
    income_count = models.IntegerField(default=0)
    expense_count = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("user", "month", "year")
        ordering = ["-year", "-month"]

    def __str__(self):
        return f"Metrics for {self.user.username} - {self.month}/{self.year}"
