from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal


class InvestmentType(models.Model):
    """Types of investments like Stocks, Bonds, Crypto, etc."""

    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Investment(models.Model):
    """Individual investment holdings"""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)  # e.g., "Apple Inc.", "Bitcoin"
    symbol = models.CharField(max_length=10, blank=True)  # e.g., "AAPL", "BTC"
    investment_type = models.ForeignKey(InvestmentType, on_delete=models.CASCADE)
    purchase_date = models.DateField()
    purchase_price = models.DecimalField(max_digits=12, decimal_places=4)
    quantity = models.DecimalField(max_digits=12, decimal_places=6)
    current_price = models.DecimalField(
        max_digits=12, decimal_places=4, null=True, blank=True
    )
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.symbol}) - {self.quantity} shares"

    @property
    def total_investment(self):
        """Total amount invested"""
        return self.purchase_price * self.quantity

    @property
    def current_value(self):
        """Current market value"""
        if self.current_price:
            return self.current_price * self.quantity
        return self.total_investment

    @property
    def profit_loss(self):
        """Profit or loss amount"""
        return self.current_value - self.total_investment

    @property
    def profit_loss_percentage(self):
        """Profit or loss percentage"""
        if self.total_investment > 0:
            return (self.profit_loss / self.total_investment) * 100
        return 0


class InvestmentTransaction(models.Model):
    """Track buy/sell transactions for investments"""

    TRANSACTION_TYPES = [
        ("BUY", "Buy"),
        ("SELL", "Sell"),
        ("DIVIDEND", "Dividend"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    investment = models.ForeignKey(Investment, on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    quantity = models.DecimalField(max_digits=12, decimal_places=6)
    price_per_unit = models.DecimalField(max_digits=12, decimal_places=4)
    transaction_date = models.DateField()
    fees = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("0.00"))
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.transaction_type} {self.quantity} {self.investment.symbol} @ {self.price_per_unit}"

    @property
    def total_amount(self):
        """Total transaction amount including fees"""
        base_amount = self.quantity * self.price_per_unit
        if self.transaction_type == "BUY":
            return base_amount + self.fees
        else:
            return base_amount - self.fees


class Portfolio(models.Model):
    """Investment portfolio grouping"""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.name}"

    @property
    def total_value(self):
        """Total current value of all investments in portfolio"""
        investments = Investment.objects.filter(user=self.user)
        return sum(inv.current_value for inv in investments)

    @property
    def total_invested(self):
        """Total amount invested in portfolio"""
        investments = Investment.objects.filter(user=self.user)
        return sum(inv.total_investment for inv in investments)

    @property
    def total_profit_loss(self):
        """Total profit/loss for portfolio"""
        return self.total_value - self.total_invested
