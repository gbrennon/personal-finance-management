
# models.py
from django.db import models
from django.contrib.auth.models import User

class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('Income','Income'),
        ('Expense','Expense'),
    ]
    INCOME_CATEGORIES = [
        ('Salary', 'Salary'),
        ('Bonus', 'Bonus'),
        ('Interest', 'Interest'),
        ('Gift', 'Gift'),
        ('Other', 'Other'),
    ]

    EXPENSE_CATEGORIES = [
        ('Food', 'Food'),
        ('Rent', 'Rent'),
        ('Utilities', 'Utilities'),
        ('Travel', 'Travel'),
        ('Shopping', 'Shopping'),
        ('Health', 'Health'),
        ('Other', 'Other'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES, default='Expense')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=100)
    type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    date = models.DateField()
    
    def __str__(self):
        return f"{self.transaction_type.capitalize()} - {self.category} - {self.amount}"

class Budget(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    month = models.IntegerField()
    year = models.IntegerField() 

    def __str__(self):
        return f"{self.user.username} - {self.month}/{self.year}: ₹{self.amount or 'Not Set'}"
    class Meta:
        unique_together = ('user', 'month', 'year')