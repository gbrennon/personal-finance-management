# finance/models.py
from django.db import models
from django.contrib.auth.models import User

# --- NEW CATEGORY MODEL ---
# This model will store all your custom income and expense categories in the database.
class Category(models.Model):
    TRANSACTION_TYPES = [
        ('Income', 'Income'),
        ('Expense', 'Expense'),
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
        unique_together = ('user', 'name', 'transaction_type')
        verbose_name_plural = "Categories"


# --- UPDATED TRANSACTION MODEL ---
class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('Income', 'Income'),
        ('Expense', 'Expense'),
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
        unique_together = ('user', 'month', 'year')