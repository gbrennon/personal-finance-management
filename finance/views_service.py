from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from datetime import date
from decimal import Decimal
from finance.infrastructure.container import container
from finance.domain.entities import TransactionType, CryptoType
import json


@login_required
def dashboard_service(request):
    """Dashboard view using service layer"""
    try:
        # Get user transactions using service
        get_transactions_service = container.get_user_transactions_service()
        transactions = get_transactions_service.execute(request.user.id)

        # Calculate totals
        total_income = sum(
            t.amount
            for t in transactions
            if t.transaction_type == TransactionType.INCOME
        )
        total_expense = sum(
            t.amount
            for t in transactions
            if t.transaction_type == TransactionType.EXPENSE
        )
        total_savings = abs(total_income - total_expense)

        return render(
            request,
            "finance/dashboard_service.html",
            {
                "transactions": transactions,
                "total_income": total_income,
                "total_expense": total_expense,
                "total_savings": total_savings,
            },
        )
    except Exception as e:
        messages.error(request, f"Error loading dashboard: {str(e)}")
        return render(
            request,
            "finance/dashboard_service.html",
            {
                "transactions": [],
                "total_income": 0,
                "total_expense": 0,
                "total_savings": 0,
            },
        )


@login_required
def add_income_service(request):
    """Add income view using service layer"""
    if request.method == "POST":
        try:
            # Extract form data
            amount = Decimal(request.POST.get("amount"))
            category_id = int(request.POST.get("category_id"))
            transaction_date = date.fromisoformat(request.POST.get("date"))

            # Use service to register transaction
            register_service = container.register_transaction_service()
            transaction = register_service.execute(
                user_id=request.user.id,
                transaction_type=TransactionType.INCOME,
                amount=amount,
                category_id=category_id,
                transaction_date=transaction_date,
            )

            messages.success(request, "Income added successfully.")
            return redirect("dashboard_service")

        except Exception as e:
            messages.error(request, f"Error adding income: {str(e)}")

    # Get income categories for the form
    try:
        category_repo = container.category_repository()
        categories = category_repo.get_by_user_and_type(request.user.id, "Income")
    except Exception:
        categories = []

    return render(
        request, "finance/add_income_service.html", {"categories": categories}
    )


@login_required
def add_expense_service(request):
    """Add expense view using service layer"""
    if request.method == "POST":
        try:
            # Extract form data
            amount = Decimal(request.POST.get("amount"))
            category_id = int(request.POST.get("category_id"))
            transaction_date = date.fromisoformat(request.POST.get("date"))

            # Use service to register transaction
            register_service = container.register_transaction_service()
            transaction = register_service.execute(
                user_id=request.user.id,
                transaction_type=TransactionType.EXPENSE,
                amount=amount,
                category_id=category_id,
                transaction_date=transaction_date,
            )

            messages.success(request, "Expense added successfully.")
            return redirect("dashboard_service")

        except Exception as e:
            messages.error(request, f"Error adding expense: {str(e)}")

    # Get expense categories for the form
    try:
        category_repo = container.category_repository()
        categories = category_repo.get_by_user_and_type(request.user.id, "Expense")
    except Exception:
        categories = []

    return render(
        request, "finance/add_expense_service.html", {"categories": categories}
    )


@login_required
def retirement_dashboard(request):
    """Retirement dashboard view"""
    try:
        # Get retirement goals using service
        get_goals_service = container.get_user_retirement_goals_service()
        goals = get_goals_service.execute(request.user.id)

        # Get recent contributions
        get_contributions_service = container.get_retirement_contributions_service()
        contributions = get_contributions_service.execute(request.user.id)

        return render(
            request,
            "finance/retirement_dashboard.html",
            {
                "goals": goals,
                "contributions": contributions[:10],  # Show last 10 contributions
            },
        )
    except Exception as e:
        messages.error(request, f"Error loading retirement dashboard: {str(e)}")
        return render(
            request,
            "finance/retirement_dashboard.html",
            {
                "goals": [],
                "contributions": [],
            },
        )


@login_required
def create_retirement_goal(request):
    """Create retirement goal view"""
    if request.method == "POST":
        try:
            # Extract form data
            target_amount = Decimal(request.POST.get("target_amount"))
            target_date = date.fromisoformat(request.POST.get("target_date"))
            monthly_contribution = Decimal(request.POST.get("monthly_contribution"))
            current_amount = Decimal(request.POST.get("current_amount", "0"))

            # Use service to create goal
            create_service = container.create_retirement_goal_service()
            goal = create_service.execute(
                user_id=request.user.id,
                target_amount=target_amount,
                target_date=target_date,
                monthly_contribution=monthly_contribution,
                current_amount=current_amount,
            )

            messages.success(request, "Retirement goal created successfully.")
            return redirect("retirement_dashboard")

        except Exception as e:
            messages.error(request, f"Error creating retirement goal: {str(e)}")

    return render(request, "finance/create_retirement_goal.html")


@login_required
def add_retirement_contribution(request):
    """Add retirement contribution view"""
    if request.method == "POST":
        try:
            # Extract form data
            goal_id = int(request.POST.get("goal_id"))
            amount = Decimal(request.POST.get("amount"))
            contribution_date = date.fromisoformat(request.POST.get("date"))
            description = request.POST.get("description", "")

            # Use service to add contribution
            add_service = container.add_retirement_contribution_service()
            contribution = add_service.execute(
                user_id=request.user.id,
                retirement_goal_id=goal_id,
                amount=amount,
                contribution_date=contribution_date,
                description=description,
            )

            messages.success(request, "Retirement contribution added successfully.")
            return redirect("retirement_dashboard")

        except Exception as e:
            messages.error(request, f"Error adding contribution: {str(e)}")

    # Get user's retirement goals for the form
    try:
        get_goals_service = container.get_user_retirement_goals_service()
        goals = get_goals_service.execute(request.user.id)
    except Exception:
        goals = []

    return render(request, "finance/add_retirement_contribution.html", {"goals": goals})


@login_required
def crypto_dashboard(request):
    """Crypto investments dashboard view"""
    try:
        # Get crypto investments using service
        get_investments_service = container.get_user_crypto_investments_service()
        investments = get_investments_service.execute(request.user.id)

        # Get portfolio summary
        get_summary_service = container.get_crypto_portfolio_summary_service()
        summary = get_summary_service.execute(request.user.id)

        return render(
            request,
            "finance/crypto_dashboard.html",
            {
                "investments": investments,
                "summary": summary,
            },
        )
    except Exception as e:
        messages.error(request, f"Error loading crypto dashboard: {str(e)}")
        return render(
            request,
            "finance/crypto_dashboard.html",
            {
                "investments": [],
                "summary": {
                    "total_invested": 0,
                    "current_value": 0,
                    "total_profit_loss": 0,
                    "btc_investments": [],
                    "eth_investments": [],
                },
            },
        )


@login_required
def add_crypto_investment(request):
    """Add crypto investment view"""
    if request.method == "POST":
        try:
            # Extract form data
            crypto_type = CryptoType(request.POST.get("crypto_type"))
            amount_invested = Decimal(request.POST.get("amount_invested"))
            quantity = Decimal(request.POST.get("quantity"))
            purchase_price = Decimal(request.POST.get("purchase_price"))
            purchase_date = date.fromisoformat(request.POST.get("purchase_date"))

            # Use service to register investment
            register_service = container.register_crypto_investment_service()
            investment = register_service.execute(
                user_id=request.user.id,
                crypto_type=crypto_type,
                amount_invested=amount_invested,
                quantity=quantity,
                purchase_price=purchase_price,
                purchase_date=purchase_date,
            )

            messages.success(request, "Crypto investment added successfully.")
            return redirect("crypto_dashboard")

        except Exception as e:
            messages.error(request, f"Error adding crypto investment: {str(e)}")

    return render(
        request,
        "finance/add_crypto_investment.html",
        {"crypto_types": [{"value": ct.value, "label": ct.value} for ct in CryptoType]},
    )


@login_required
@require_http_methods(["POST"])
def update_crypto_price(request, investment_id):
    """Update crypto price via AJAX"""
    try:
        data = json.loads(request.body)
        current_price = Decimal(str(data.get("current_price")))

        # Use service to update price
        update_service = container.update_crypto_price_service()
        investment = update_service.execute(investment_id, current_price)

        return JsonResponse(
            {
                "success": True,
                "current_value": float(investment.current_value or 0),
                "profit_loss": float(investment.profit_loss or 0),
            }
        )

    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=400)


@login_required
@require_http_methods(["POST"])
def sell_crypto_investment(request, investment_id):
    """Sell crypto investment"""
    try:
        data = json.loads(request.body)
        sell_price = Decimal(str(data.get("sell_price")))

        # Use service to sell investment
        sell_service = container.sell_crypto_investment_service()
        result = sell_service.execute(investment_id, request.user.id, sell_price)

        return JsonResponse(
            {
                "success": True,
                "sale_value": float(result["sale_value"]),
                "profit_loss": float(result["profit_loss"]),
                "profit_loss_percentage": float(result["profit_loss_percentage"]),
            }
        )

    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=400)
