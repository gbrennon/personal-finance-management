from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum, Q
from .models import BankAccount, BankTransaction, BankTransfer, BankInstitution
from .forms import BankAccountForm, BankTransactionForm, BankTransferForm


@login_required
def banks_dashboard(request):
    """Main banks dashboard"""
    accounts = BankAccount.objects.filter(user=request.user, is_active=True)

    # Calculate totals by account type
    checking_total = (
        accounts.filter(account_type="CHECKING").aggregate(Sum("current_balance"))[
            "current_balance__sum"
        ]
        or 0
    )
    savings_total = (
        accounts.filter(account_type="SAVINGS").aggregate(Sum("current_balance"))[
            "current_balance__sum"
        ]
        or 0
    )
    credit_total = (
        accounts.filter(account_type__in=["CREDIT_CARD", "LINE_OF_CREDIT"]).aggregate(
            Sum("current_balance")
        )["current_balance__sum"]
        or 0
    )

    # Recent transactions
    recent_transactions = BankTransaction.objects.filter(user=request.user)[:10]

    context = {
        "accounts": accounts,
        "checking_total": checking_total,
        "savings_total": savings_total,
        "credit_total": credit_total,
        "recent_transactions": recent_transactions,
    }
    return render(request, "banks/dashboard.html", context)


@login_required
def account_list(request):
    """List all bank accounts"""
    accounts = BankAccount.objects.filter(user=request.user)
    return render(request, "banks/account_list.html", {"accounts": accounts})


@login_required
def add_account(request):
    """Add a new bank account"""
    if request.method == "POST":
        form = BankAccountForm(request.POST)
        if form.is_valid():
            account = form.save(commit=False)
            account.user = request.user
            account.save()
            messages.success(request, "Bank account added successfully!")
            return redirect("banks:dashboard")
    else:
        form = BankAccountForm()

    return render(request, "banks/add_account.html", {"form": form})


@login_required
def account_detail(request, account_id):
    """View bank account details"""
    account = get_object_or_404(BankAccount, id=account_id, user=request.user)
    transactions = BankTransaction.objects.filter(account=account)[:20]

    # Calculate monthly totals
    monthly_income = (
        transactions.filter(
            transaction_type__in=["DEPOSIT", "CREDIT", "INTEREST"]
        ).aggregate(Sum("amount"))["amount__sum"]
        or 0
    )

    monthly_expenses = (
        transactions.filter(
            transaction_type__in=["WITHDRAWAL", "PAYMENT", "FEE", "DEBIT"]
        ).aggregate(Sum("amount"))["amount__sum"]
        or 0
    )

    context = {
        "account": account,
        "transactions": transactions,
        "monthly_income": monthly_income,
        "monthly_expenses": abs(monthly_expenses),
    }
    return render(request, "banks/account_detail.html", context)


@login_required
def add_transaction(request, account_id):
    """Add a transaction to a bank account"""
    account = get_object_or_404(BankAccount, id=account_id, user=request.user)

    if request.method == "POST":
        form = BankTransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.account = account
            transaction.save()
            messages.success(request, "Transaction added successfully!")
            return redirect("banks:account_detail", account_id=account.id)
    else:
        form = BankTransactionForm()

    context = {
        "form": form,
        "account": account,
    }
    return render(request, "banks/add_transaction.html", context)


@login_required
def transfer_money(request):
    """Transfer money between accounts"""
    user_accounts = BankAccount.objects.filter(user=request.user, is_active=True)

    if request.method == "POST":
        form = BankTransferForm(request.POST, user=request.user)
        if form.is_valid():
            transfer = form.save(commit=False)
            transfer.user = request.user
            transfer.save()
            messages.success(request, "Transfer completed successfully!")
            return redirect("banks:dashboard")
    else:
        form = BankTransferForm(user=request.user)

    context = {
        "form": form,
        "user_accounts": user_accounts,
    }
    return render(request, "banks/transfer.html", context)


@login_required
def transactions_list(request):
    """List all transactions with filtering"""
    transactions = BankTransaction.objects.filter(user=request.user)

    # Filter by account if specified
    account_id = request.GET.get("account")
    if account_id:
        transactions = transactions.filter(account_id=account_id)

    # Filter by transaction type if specified
    transaction_type = request.GET.get("type")
    if transaction_type:
        transactions = transactions.filter(transaction_type=transaction_type)

    # Search functionality
    search = request.GET.get("search")
    if search:
        transactions = transactions.filter(
            Q(description__icontains=search) | Q(category__icontains=search)
        )

    transactions = transactions[:50]  # Limit to 50 results
    user_accounts = BankAccount.objects.filter(user=request.user)

    context = {
        "transactions": transactions,
        "user_accounts": user_accounts,
        "selected_account": account_id,
        "selected_type": transaction_type,
        "search_query": search,
    }
    return render(request, "banks/transactions_list.html", context)


@login_required
def account_summary(request):
    """Account summary and analytics"""
    accounts = BankAccount.objects.filter(user=request.user)

    # Calculate account type totals
    account_summary = {}
    for account in accounts:
        acc_type = account.get_account_type_display()
        if acc_type not in account_summary:
            account_summary[acc_type] = {"count": 0, "total_balance": 0, "accounts": []}
        account_summary[acc_type]["count"] += 1
        account_summary[acc_type]["total_balance"] += account.current_balance
        account_summary[acc_type]["accounts"].append(account)

    context = {
        "account_summary": account_summary,
        "total_accounts": accounts.count(),
    }
    return render(request, "banks/summary.html", context)
