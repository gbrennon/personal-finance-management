from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal


class BankInstitution(models.Model):
    """Bank institutions/financial institutions"""

    name = models.CharField(max_length=100, unique=True)
    routing_number = models.CharField(max_length=9, blank=True)
    website = models.URLField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]


class BankAccount(models.Model):
    """User's bank accounts"""

    ACCOUNT_TYPES = [
        ("CHECKING", "Checking"),
        ("SAVINGS", "Savings"),
        ("MONEY_MARKET", "Money Market"),
        ("CD", "Certificate of Deposit"),
        ("CREDIT_CARD", "Credit Card"),
        ("LINE_OF_CREDIT", "Line of Credit"),
        ("LOAN", "Loan"),
        ("MORTGAGE", "Mortgage"),
        ("OTHER", "Other"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    institution = models.ForeignKey(BankInstitution, on_delete=models.CASCADE)
    account_name = models.CharField(max_length=100)
    account_type = models.CharField(max_length=20, choices=ACCOUNT_TYPES)
    account_number = models.CharField(max_length=50, blank=True)
    current_balance = models.DecimalField(max_digits=12, decimal_places=2)
    available_balance = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True
    )
    credit_limit = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="For credit accounts",
    )
    interest_rate = models.DecimalField(
        max_digits=6,
        decimal_places=3,
        null=True,
        blank=True,
        help_text="Annual interest rate percentage",
    )
    minimum_balance = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    monthly_fee = models.DecimalField(
        max_digits=8, decimal_places=2, default=Decimal("0.00")
    )
    is_active = models.BooleanField(default=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.account_name} - {self.institution.name}"

    @property
    def available_credit(self):
        """Available credit for credit accounts"""
        if self.credit_limit and self.account_type in ["CREDIT_CARD", "LINE_OF_CREDIT"]:
            return (
                self.credit_limit + self.current_balance
            )  # Balance is negative for credit cards
        return None

    @property
    def utilization_rate(self):
        """Credit utilization rate for credit accounts"""
        if self.credit_limit and self.account_type in ["CREDIT_CARD", "LINE_OF_CREDIT"]:
            if self.credit_limit > 0:
                used_credit = abs(self.current_balance)
                return (used_credit / self.credit_limit) * 100
        return None

    class Meta:
        unique_together = ("user", "account_name", "institution")
        ordering = ["institution__name", "account_name"]


class BankTransaction(models.Model):
    """Bank account transactions"""

    TRANSACTION_TYPES = [
        ("DEPOSIT", "Deposit"),
        ("WITHDRAWAL", "Withdrawal"),
        ("TRANSFER", "Transfer"),
        ("PAYMENT", "Payment"),
        ("FEE", "Fee"),
        ("INTEREST", "Interest"),
        ("DIVIDEND", "Dividend"),
        ("ATM", "ATM"),
        ("CHECK", "Check"),
        ("DEBIT", "Debit Card"),
        ("CREDIT", "Credit"),
        ("OTHER", "Other"),
    ]

    STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("CLEARED", "Cleared"),
        ("CANCELLED", "Cancelled"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    account = models.ForeignKey(BankAccount, on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    description = models.CharField(max_length=200)
    transaction_date = models.DateField()
    posted_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="CLEARED")
    reference_number = models.CharField(max_length=50, blank=True)
    category = models.CharField(max_length=100, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.account.account_name} - {self.description} - ${self.amount}"

    class Meta:
        ordering = ["-transaction_date", "-created_at"]


class BankTransfer(models.Model):
    """Track transfers between accounts"""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    from_account = models.ForeignKey(
        BankAccount, on_delete=models.CASCADE, related_name="transfers_out"
    )
    to_account = models.ForeignKey(
        BankAccount, on_delete=models.CASCADE, related_name="transfers_in"
    )
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    transfer_date = models.DateField()
    description = models.CharField(max_length=200, blank=True)
    fee = models.DecimalField(max_digits=8, decimal_places=2, default=Decimal("0.00"))
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Transfer: {self.from_account.account_name} → {self.to_account.account_name} - ${self.amount}"

    class Meta:
        ordering = ["-transfer_date"]


class RecurringTransaction(models.Model):
    """Recurring transactions like direct deposits, automatic payments"""

    FREQUENCY_CHOICES = [
        ("WEEKLY", "Weekly"),
        ("BIWEEKLY", "Bi-weekly"),
        ("MONTHLY", "Monthly"),
        ("QUARTERLY", "Quarterly"),
        ("ANNUALLY", "Annually"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    account = models.ForeignKey(BankAccount, on_delete=models.CASCADE)
    description = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    frequency = models.CharField(max_length=20, choices=FREQUENCY_CHOICES)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    next_occurrence = models.DateField()
    is_active = models.BooleanField(default=True)
    category = models.CharField(max_length=100, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.description} - ${self.amount} ({self.get_frequency_display()})"

    class Meta:
        ordering = ["next_occurrence"]


class BankAlert(models.Model):
    """Bank account alerts and notifications"""

    ALERT_TYPES = [
        ("LOW_BALANCE", "Low Balance"),
        ("HIGH_BALANCE", "High Balance"),
        ("LARGE_TRANSACTION", "Large Transaction"),
        ("OVERDRAFT", "Overdraft"),
        ("PAYMENT_DUE", "Payment Due"),
        ("UNUSUAL_ACTIVITY", "Unusual Activity"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    account = models.ForeignKey(
        BankAccount, on_delete=models.CASCADE, null=True, blank=True
    )
    alert_type = models.CharField(max_length=20, choices=ALERT_TYPES)
    threshold_amount = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True
    )
    is_active = models.BooleanField(default=True)
    email_notification = models.BooleanField(default=True)
    sms_notification = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        account_name = self.account.account_name if self.account else "All Accounts"
        return f"{self.get_alert_type_display()} - {account_name}"

    class Meta:
        unique_together = ("user", "account", "alert_type")
