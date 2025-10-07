from django.urls import path
from . import views

app_name = "investments"

urlpatterns = [
    path("", views.investments_dashboard, name="dashboard"),
    path("list/", views.investment_list, name="investment_list"),
    path("add/", views.add_investment, name="add_investment"),
    path("<int:investment_id>/", views.investment_detail, name="investment_detail"),
    path(
        "<int:investment_id>/add-transaction/",
        views.add_transaction,
        name="add_transaction",
    ),
    path("portfolio/", views.portfolio_view, name="portfolio"),
]
