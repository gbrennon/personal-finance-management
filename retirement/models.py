from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal
from datetime import date


class RetirementAccount(models.Model):
    """Different types of retirement accounts"""

    ACCOUNT_TYPES = [
        ("401K", "401(k)"),
        ("IRA", "Traditional IRA"),
        ("ROTH_IRA", "Roth IRA"),
        ("403B", "403(b)"),
        ("SEP_IRA", "SEP-IRA"),
        ("SIMPLE_IRA", "SIMPLE IRA"),
        ("PENSION", "Pension"),
        ("OTHER", "Other"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    account_name = models.CharField(max_length=100)
    account_type = models.CharField(max_length=20, choices=ACCOUNT_TYPES)
    provider = models.CharField(
        max_length=100, blank=True
    )  # e.g., "Fidelity", "Vanguard"
    account_number = models.CharField(max_length=50, blank=True)
    current_balance = models.DecimalField(max_digits=12, decimal_places=2)
    employer_match_rate = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Employer match percentage",
    )
    vesting_schedule = models.TextField(
        blank=True, help_text="Vesting schedule details"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.account_name} ({self.get_account_type_display()})"

    class Meta:
        unique_together = ("user", "account_name")


class RetirementContribution(models.Model):
    """Track contributions to retirement accounts"""

    CONTRIBUTION_TYPES = [
        ("EMPLOYEE", "Employee Contribution"),
        ("EMPLOYER", "Employer Match"),
        ("ROLLOVER", "Rollover"),
        ("CATCH_UP", "Catch-up Contribution"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    account = models.ForeignKey(RetirementAccount, on_delete=models.CASCADE)
    contribution_type = models.CharField(max_length=20, choices=CONTRIBUTION_TYPES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    contribution_date = models.DateField()
    tax_year = models.IntegerField()
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.account.account_name} - {self.get_contribution_type_display()} - ${self.amount}"

    class Meta:
        ordering = ["-contribution_date"]


class RetirementGoal(models.Model):
    """User's retirement planning goals"""

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    target_retirement_age = models.IntegerField(default=65)
    target_retirement_amount = models.DecimalField(max_digits=12, decimal_places=2)
    current_age = models.IntegerField()
    annual_income = models.DecimalField(max_digits=10, decimal_places=2)
    expected_annual_return = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=Decimal("7.00"),
        help_text="Expected annual return percentage",
    )
    inflation_rate = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=Decimal("3.00"),
        help_text="Expected inflation rate percentage",
    )
    retirement_income_replacement = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=Decimal("80.00"),
        help_text="Percentage of current income needed in retirement",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Retirement Goal"

    @property
    def years_to_retirement(self):
        """Calculate years until retirement"""
        return max(0, self.target_retirement_age - self.current_age)

    @property
    def total_current_savings(self):
        """Total current retirement savings across all accounts"""
        accounts = RetirementAccount.objects.filter(user=self.user)
        return sum(account.current_balance for account in accounts)

    @property
    def monthly_savings_needed(self):
        """Calculate monthly savings needed to reach retirement goal"""
        if self.years_to_retirement <= 0:
            return 0

        # Simple calculation - can be made more sophisticated
        remaining_amount = self.target_retirement_amount - self.total_current_savings
        months_to_retirement = self.years_to_retirement * 12

        if months_to_retirement > 0:
            return remaining_amount / months_to_retirement
        return 0

    @property
    def retirement_readiness_percentage(self):
        """Calculate what percentage of retirement goal is currently saved"""
        if self.target_retirement_amount > 0:
            return (self.total_current_savings / self.target_retirement_amount) * 100
        return 0


class RetirementProjection(models.Model):
    """Store retirement projections and scenarios"""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    scenario_name = models.CharField(max_length=100)
    monthly_contribution = models.DecimalField(max_digits=10, decimal_places=2)
    annual_return_rate = models.DecimalField(max_digits=5, decimal_places=2)
    years_to_retirement = models.IntegerField()
    projected_balance = models.DecimalField(max_digits=12, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.scenario_name}"

    class Meta:
        ordering = ["-created_at"]


class SocialSecurityEstimate(models.Model):
    """Store Social Security benefit estimates"""

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    estimated_monthly_benefit = models.DecimalField(max_digits=8, decimal_places=2)
    full_retirement_age = models.IntegerField(default=67)
    early_retirement_benefit = models.DecimalField(
        max_digits=8, decimal_places=2, null=True, blank=True
    )
    delayed_retirement_benefit = models.DecimalField(
        max_digits=8, decimal_places=2, null=True, blank=True
    )
    last_updated = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s Social Security Estimate"
