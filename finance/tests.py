# tests.py
from django.test import TestCase
from django.contrib.auth.models import User
from .models import Transaction, Budget
from datetime import date

from finance import models

class FinanceTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        Transaction.objects.create(user=self.user, amount=1000, category='Salary', type='Income', date=date.today())
        Transaction.objects.create(user=self.user, amount=500, category='Food', type='Expense', date=date.today())

    def test_transaction_sum(self):
        income = Transaction.objects.filter(user=self.user, type='Income').aggregate(total=models.Sum('amount'))['total']
        expense = Transaction.objects.filter(user=self.user, type='Expense').aggregate(total=models.Sum('amount'))['total']
        self.assertEqual(income, 1000)
        self.assertEqual(expense, 500)

    def test_dashboard_access(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get('/dashboard/')
        self.assertEqual(response.status_code, 200)

