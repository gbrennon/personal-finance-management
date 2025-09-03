# views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Transaction, Budget
from .forms import TransactionForm, BudgetForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from datetime import date, timedelta
from django.db.models.functions import ExtractMonth, ExtractYear
from django.db.models import Sum
import pandas as pd
from sklearn.linear_model import LinearRegression
import datetime
import json
from decimal import Decimal
from django.db.models.functions import TruncMonth, TruncYear
from django.utils import timezone
from django.contrib import messages
from finance import models
from collections import defaultdict


def home_view(request):
    print("🏠 home_view loaded")
    if request.user.is_authenticated:
        print("🏠 home_view loaded")
        return redirect('dashboard')
    return render(request, 'finance/home.html')

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'finance/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'finance/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def dashboard(request):
     transactions = Transaction.objects.filter(user=request.user).order_by('-date')

     total_income = Transaction.objects.filter(user=request.user, transaction_type__iexact='Income').aggregate(Sum('amount'))['amount__sum'] or 0
     total_expense = Transaction.objects.filter(user=request.user, transaction_type__iexact='Expense').aggregate(Sum('amount'))['amount__sum'] or 0
     total_savings =abs(total_income - total_expense)

     return render(request, 'finance/dashboard.html', {
        'transactions': transactions,
        'total_income': total_income,
        'total_expense': total_expense,
        'total_savings': total_savings,
    })

@login_required
def add_income(request):
    if request.method == 'POST':
        # Pass the current user to the form
        form = TransactionForm(request.POST, user=request.user, transaction_type='Income')
        if form.is_valid():
            income = form.save(commit=False)
            income.user = request.user
            income.transaction_type = 'Income'
            income.save()
            return redirect('dashboard')
    else:
        # Also pass the current user when displaying the empty form
        form = TransactionForm(user=request.user, transaction_type='Income')
    return render(request, 'finance/add_income.html', {'form': form})
    

# finance/views.py

@login_required
def add_expense(request):
    if request.method == 'POST':
        # Pass the user to the form to correctly filter categories
        form = TransactionForm(request.POST, user=request.user, transaction_type='Expense')
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            expense.transaction_type = 'Expense'
            # Ensure date is set before saving and using it
            if not expense.date:
                expense.date = timezone.now().date()
            
            # Save the expense first to include it in the monthly total
            expense.save() 
            
            month = expense.date.month
            year = expense.date.year

            # Budget Check
            budget = Budget.objects.filter(
                user=request.user,
                month=month,
                year=year
            ).first()

            # Only perform the budget check if a budget is set for that month
            if budget and budget.amount is not None:
                monthly_expense = Transaction.objects.filter(
                    user=request.user,
                    transaction_type='Expense',
                    date__month=month,
                    date__year=year
                ).aggregate(total=Sum('amount'))['total'] or 0

                if monthly_expense > budget.amount:
                    messages.warning(
                        request, 
                        f'⚠️ Alert: You have now exceeded your monthly budget of {budget.amount}.'
                    )
            
            messages.success(request, "✅ Expense added successfully.")
            return redirect('dashboard')
    else:
        # Also pass the user when displaying the empty form
        form = TransactionForm(user=request.user, transaction_type='Expense')
        
    return render(request, 'finance/add_expense.html', {'form': form})


    
@login_required
def edit_transaction(request, transaction_id):
    transaction = get_object_or_404(Transaction, id=transaction_id, user=request.user)
    
    if request.method == 'POST':
        # Pass the user and transaction type to the form
        form = TransactionForm(
            request.POST, 
            instance=transaction, 
            user=request.user, 
            transaction_type=transaction.transaction_type
        )
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        # Also pass the user and transaction type when displaying the form
        form = TransactionForm(
            instance=transaction, 
            user=request.user, 
            transaction_type=transaction.transaction_type
        )
        
    return render(request, 'finance/edit_transaction.html', {'form': form, 'transaction': transaction})


@login_required
def delete_transaction(request, transaction_id):
    transaction = get_object_or_404(Transaction, id=transaction_id, user=request.user)
    
    if request.method == 'POST':
        # If the user confirms the deletion via the form, then delete
        transaction.delete()
        messages.success(request, "Transaction deleted successfully.")
        return redirect('dashboard')
        
    # If it's a GET request, show a confirmation page
    return render(request, 'finance/delete_confirm.html', {'transaction': transaction})


def forecast(request):
    user = request.user

    # Get aggregated expenses per month
    monthly_expense = (
        Transaction.objects.filter(user=user, transaction_type__iexact='Expense')
        .annotate(month=TruncMonth('date'))
        .values('month')
        .annotate(total=Sum('amount'))
        .order_by('month')
    )

    if len(monthly_expense) < 2:
        return render(request, 'finance/forecast.html', {
            'past_labels': json.dumps([]),
            'past_values': json.dumps([]),
            'forecast_labels': json.dumps([]),
            'forecast_values': json.dumps([]),
            'warning': 'Not enough data for forecasting.'
        })

    # Convert to DataFrame
    df = pd.DataFrame(monthly_expense)
    df['month'] = pd.to_datetime(df['month'])
    df['month_str'] = df['month'].dt.strftime('%b %Y')
    df['month_num'] = range(len(df))

    # Train Linear Regression
    X = df[['month_num']]
    y = df['total'].astype(float)

    model = LinearRegression()
    model.fit(X, y)

    # Forecast for next 3 months
    future_months = list(range(len(df), len(df) + 3))
    forecast_values = model.predict(pd.DataFrame({'month_num': future_months}))
    forecast_labels = pd.date_range(
        start=df['month'].iloc[-1] + pd.DateOffset(months=1),
        periods=3,
        freq='MS'
    ).strftime('%b %Y').tolist()

    # Get next month's prediction separately
    next_month_label = forecast_labels[0]
    next_month_value = round(float(forecast_values[0]), 2)

    # Prepare chart data
    past_labels = df['month_str'].tolist()
    past_values = [float(val) for val in df['total']]

    context = {
        'past_labels': json.dumps(past_labels),
        'past_values': json.dumps(past_values),
        'forecast_labels': json.dumps(forecast_labels),
        'forecast_values': json.dumps([round(float(x), 2) for x in forecast_values]),
        'predicted_total': next_month_value,
        'predicted_month': next_month_label,
    }

    return render(request, 'finance/forecast.html', context)

def add_budget(request):
    if request.method == 'POST':
        form = BudgetForm(request.POST)
        if form.is_valid():
            budget = form.save(commit=False)
            budget.user = request.user
            budget.save()
            messages.success(request, "Budget set successfully.")
            return redirect('dashboard')
    else:
        form = BudgetForm()

    return render(request, 'finance/add_budget.html', {'form': form})

@login_required
def edit_budget(request, month, year):
    user = request.user

    budget_obj = Budget.objects.filter(user=user, month=month, year=year).first()
    current_budget = budget_obj.amount if budget_obj else None

    if request.method == 'POST':
        budget_value = request.POST.get('budget')

        if budget_value == '':
            budget_value = None
        else:
            try:
                budget_value = float(budget_value)
            except ValueError:
                messages.error(request, "Invalid budget value.")
                return redirect('report')

        Budget.objects.update_or_create(
            user=user,
            month=month,
            year=year,
            defaults={'amount': budget_value}
        )

        messages.success(request, "Budget updated successfully!")
        return redirect('report')

    return render(request, 'finance/edit_budget.html', {
        'month': month,
        'year': year,
        'budget': current_budget
    })

@login_required
def report(request):
    user = request.user

    # Get all transactions grouped by month and type
    transactions = (
        Transaction.objects.filter(user=user)
        .annotate(month=TruncMonth('date'))
        .values('month', 'transaction_type')
        .annotate(total=Sum('amount'))
        .order_by('month')
    )

    # Organize by month
    monthly = defaultdict(lambda: {'Income': 0, 'Expense': 0})
    months_seen = set()

    for tx in transactions:
        month = tx['month']
        tx_type = tx['transaction_type'].capitalize()
        monthly[month][tx_type] = tx['total']
        months_seen.add(month)

    # Build structured list
    monthly_data = []
    for date in sorted(months_seen):
        income = monthly[date].get('Income', 0)
        expense = monthly[date].get('Expense', 0)
        savings = abs(income - expense)

        # Get monthly budget (not category-wise)
        budget_obj = Budget.objects.filter(user=user, month=date.month, year=date.year).first()

        monthly_data.append({
            'month': date.strftime('%B %Y'),
            'month_num': date.month,
            'year': date.year,
            'income': round(income, 2),
            'expense': round(expense, 2),
            'budget': budget_obj.amount if budget_obj else None,
            'savings': round(savings, 2),
            'budget': budget_obj.amount if budget_obj else None,
            'over_budget': budget_obj and budget_obj.amount is not None and expense > budget_obj.amount
        })

    # Totals
    total_income = sum(item['income'] for item in monthly_data)
    total_expense = sum(item['expense'] for item in monthly_data)
    total_savings = abs(total_income - total_expense)

    # Budget alerts (current month only)
    current_month = timezone.now().month
    current_year = timezone.now().year
    budgets = Budget.objects.filter(user=user, month=current_month, year=current_year)
    over_budget = []

    for b in budgets:
        total_spent = Transaction.objects.filter(
            user=user,
            transaction_type='Expense',
            date__month=current_month,
            date__year=current_year
        ).aggregate(total=Sum('amount'))['total'] or 0

        if total_spent > b.amount:
            over_budget.append(b.category)

    context = {
        'monthly_data': monthly_data,
        'total_income': round(total_income, 2),
        'total_expense': round(total_expense, 2),
        'total_savings': round(total_savings, 2),
        'over_budget': over_budget,
    }

    return render(request, 'finance/report.html', context)