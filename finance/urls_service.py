from django.urls import path
from . import views_service

urlpatterns = [
    # Dashboard
    path("dashboard/", views_service.dashboard_service, name="dashboard_service"),
    # Transaction management
    path("add-income/", views_service.add_income_service, name="add_income_service"),
    path("add-expense/", views_service.add_expense_service, name="add_expense_service"),
    # Retirement planning
    path(
        "retirement/", views_service.retirement_dashboard, name="retirement_dashboard"
    ),
    path(
        "retirement/create-goal/",
        views_service.create_retirement_goal,
        name="create_retirement_goal",
    ),
    path(
        "retirement/add-contribution/",
        views_service.add_retirement_contribution,
        name="add_retirement_contribution",
    ),
    # Crypto investments
    path("crypto/", views_service.crypto_dashboard, name="crypto_dashboard"),
    path(
        "crypto/add-investment/",
        views_service.add_crypto_investment,
        name="add_crypto_investment",
    ),
    path(
        "crypto/update-price/<int:investment_id>/",
        views_service.update_crypto_price,
        name="update_crypto_price",
    ),
    path(
        "crypto/sell/<int:investment_id>/",
        views_service.sell_crypto_investment,
        name="sell_crypto_investment",
    ),
]
