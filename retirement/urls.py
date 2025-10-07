from django.urls import path
from . import views

app_name = "retirement"

urlpatterns = [
    path("", views.retirement_dashboard, name="dashboard"),
    path("accounts/", views.account_list, name="account_list"),
    path("accounts/add/", views.add_account, name="add_account"),
    path("accounts/<int:account_id>/", views.account_detail, name="account_detail"),
    path(
        "accounts/<int:account_id>/add-contribution/",
        views.add_contribution,
        name="add_contribution",
    ),
    path("planning/", views.retirement_planning, name="planning"),
    path("calculator/", views.retirement_calculator, name="calculator"),
]
