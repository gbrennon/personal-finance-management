# urls.py (in finance app)
from django.urls import path, include
from . import views
from .views import home_view, register_view, login_view, dashboard, logout_view


urlpatterns = [
    path("", views.home_view, name="home"),
    path("register/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("add_income/", views.add_income, name="add_income"),
    path("add_expense/", views.add_expense, name="add_expense"),
    path(
        "edit_transaction/<int:transaction_id>/",
        views.edit_transaction,
        name="edit_transaction",
    ),
    path(
        "delete_transaction/<int:transaction_id>/",
        views.delete_transaction,
        name="delete_transaction",
    ),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("forecast/", views.forecast, name="forecast"),
    path("report/", views.report, name="report"),
    path("add_budget/", views.add_budget, name="add_budget"),
    path("edit_budget/<int:month>/<int:year>/", views.edit_budget, name="edit_budget"),
    # Service-based URLs
    path("service/", include("finance.urls_service")),
]
