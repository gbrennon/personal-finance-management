from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum
from .models import (
    RetirementAccount,
    RetirementContribution,
    RetirementGoal,
    SocialSecurityEstimate,
)
from .forms import RetirementAccountForm, RetirementContributionForm, RetirementGoalForm


@login_required
def retirement_dashboard(request):
    """Main retirement dashboard"""
    accounts = RetirementAccount.objects.filter(user=request.user)

    # Calculate totals
    total_balance = sum(account.current_balance for account in accounts)

    # Get retirement goal
    try:
        retirement_goal = RetirementGoal.objects.get(user=request.user)
    except RetirementGoal.DoesNotExist:
        retirement_goal = None

    # Recent contributions
    recent_contributions = RetirementContribution.objects.filter(user=request.user)[:5]

    context = {
        "accounts": accounts,
        "total_balance": total_balance,
        "retirement_goal": retirement_goal,
        "recent_contributions": recent_contributions,
    }
    return render(request, "retirement/dashboard.html", context)


@login_required
def account_list(request):
    """List all retirement accounts"""
    accounts = RetirementAccount.objects.filter(user=request.user)
    return render(request, "retirement/account_list.html", {"accounts": accounts})


@login_required
def add_account(request):
    """Add a new retirement account"""
    if request.method == "POST":
        form = RetirementAccountForm(request.POST)
        if form.is_valid():
            account = form.save(commit=False)
            account.user = request.user
            account.save()
            messages.success(request, "Retirement account added successfully!")
            return redirect("retirement:dashboard")
    else:
        form = RetirementAccountForm()

    return render(request, "retirement/add_account.html", {"form": form})


@login_required
def account_detail(request, account_id):
    """View retirement account details"""
    account = get_object_or_404(RetirementAccount, id=account_id, user=request.user)
    contributions = RetirementContribution.objects.filter(account=account)

    # Calculate total contributions
    total_contributions = contributions.aggregate(Sum("amount"))["amount__sum"] or 0

    context = {
        "account": account,
        "contributions": contributions,
        "total_contributions": total_contributions,
    }
    return render(request, "retirement/account_detail.html", context)


@login_required
def add_contribution(request, account_id):
    """Add a contribution to a retirement account"""
    account = get_object_or_404(RetirementAccount, id=account_id, user=request.user)

    if request.method == "POST":
        form = RetirementContributionForm(request.POST)
        if form.is_valid():
            contribution = form.save(commit=False)
            contribution.user = request.user
            contribution.account = account
            contribution.save()
            messages.success(request, "Contribution added successfully!")
            return redirect("retirement:account_detail", account_id=account.id)
    else:
        form = RetirementContributionForm()

    context = {
        "form": form,
        "account": account,
    }
    return render(request, "retirement/add_contribution.html", context)


@login_required
def retirement_planning(request):
    """Retirement planning and goals"""
    try:
        retirement_goal = RetirementGoal.objects.get(user=request.user)
    except RetirementGoal.DoesNotExist:
        retirement_goal = None

    if request.method == "POST":
        if retirement_goal:
            form = RetirementGoalForm(request.POST, instance=retirement_goal)
        else:
            form = RetirementGoalForm(request.POST)

        if form.is_valid():
            goal = form.save(commit=False)
            goal.user = request.user
            goal.save()
            messages.success(request, "Retirement goal updated successfully!")
            return redirect("retirement:planning")
    else:
        if retirement_goal:
            form = RetirementGoalForm(instance=retirement_goal)
        else:
            form = RetirementGoalForm()

    context = {
        "form": form,
        "retirement_goal": retirement_goal,
    }
    return render(request, "retirement/planning.html", context)


@login_required
def retirement_calculator(request):
    """Retirement calculator and projections"""
    try:
        retirement_goal = RetirementGoal.objects.get(user=request.user)
    except RetirementGoal.DoesNotExist:
        retirement_goal = None

    # Simple retirement calculation
    projection_data = None
    if retirement_goal:
        current_savings = retirement_goal.total_current_savings
        years_to_retirement = retirement_goal.years_to_retirement
        monthly_needed = retirement_goal.monthly_savings_needed

        projection_data = {
            "current_savings": current_savings,
            "years_to_retirement": years_to_retirement,
            "monthly_needed": monthly_needed,
            "target_amount": retirement_goal.target_retirement_amount,
            "readiness_percentage": retirement_goal.retirement_readiness_percentage,
        }

    context = {
        "retirement_goal": retirement_goal,
        "projection_data": projection_data,
    }
    return render(request, "retirement/calculator.html", context)
