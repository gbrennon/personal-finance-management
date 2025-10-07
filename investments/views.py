from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum
from .models import Investment, InvestmentType, InvestmentTransaction, Portfolio
from .forms import InvestmentForm, InvestmentTransactionForm


@login_required
def investments_dashboard(request):
    """Main investments dashboard"""
    investments = Investment.objects.filter(user=request.user)

    # Calculate totals
    total_invested = sum(inv.total_investment for inv in investments)
    total_current_value = sum(inv.current_value for inv in investments)
    total_profit_loss = total_current_value - total_invested

    # Recent transactions
    recent_transactions = InvestmentTransaction.objects.filter(user=request.user)[:5]

    context = {
        "investments": investments,
        "total_invested": total_invested,
        "total_current_value": total_current_value,
        "total_profit_loss": total_profit_loss,
        "recent_transactions": recent_transactions,
    }
    return render(request, "investments/dashboard.html", context)


@login_required
def investment_list(request):
    """List all investments"""
    investments = Investment.objects.filter(user=request.user)
    return render(
        request, "investments/investment_list.html", {"investments": investments}
    )


@login_required
def add_investment(request):
    """Add a new investment"""
    if request.method == "POST":
        form = InvestmentForm(request.POST)
        if form.is_valid():
            investment = form.save(commit=False)
            investment.user = request.user
            investment.save()
            messages.success(request, "Investment added successfully!")
            return redirect("investments:dashboard")
    else:
        form = InvestmentForm()

    return render(request, "investments/add_investment.html", {"form": form})


@login_required
def investment_detail(request, investment_id):
    """View investment details"""
    investment = get_object_or_404(Investment, id=investment_id, user=request.user)
    transactions = InvestmentTransaction.objects.filter(investment=investment)

    context = {
        "investment": investment,
        "transactions": transactions,
    }
    return render(request, "investments/investment_detail.html", context)


@login_required
def add_transaction(request, investment_id):
    """Add a transaction for an investment"""
    investment = get_object_or_404(Investment, id=investment_id, user=request.user)

    if request.method == "POST":
        form = InvestmentTransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.investment = investment
            transaction.save()
            messages.success(request, "Transaction added successfully!")
            return redirect(
                "investments:investment_detail", investment_id=investment.id
            )
    else:
        form = InvestmentTransactionForm()

    context = {
        "form": form,
        "investment": investment,
    }
    return render(request, "investments/add_transaction.html", context)


@login_required
def portfolio_view(request):
    """View portfolio summary"""
    investments = Investment.objects.filter(user=request.user)

    # Group by investment type
    portfolio_data = {}
    for investment in investments:
        inv_type = investment.investment_type.name
        if inv_type not in portfolio_data:
            portfolio_data[inv_type] = {
                "investments": [],
                "total_invested": 0,
                "total_current_value": 0,
            }

        portfolio_data[inv_type]["investments"].append(investment)
        portfolio_data[inv_type]["total_invested"] += investment.total_investment
        portfolio_data[inv_type]["total_current_value"] += investment.current_value

    # Calculate profit/loss for each type
    for inv_type in portfolio_data:
        portfolio_data[inv_type]["profit_loss"] = (
            portfolio_data[inv_type]["total_current_value"]
            - portfolio_data[inv_type]["total_invested"]
        )

    context = {
        "portfolio_data": portfolio_data,
    }
    return render(request, "investments/portfolio.html", context)
