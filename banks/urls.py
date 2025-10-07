from django.urls import path
from . import views

app_name = "banks"

urlpatterns = [
    path("", views.banks_dashboard, name="dashboard"),
    path("accounts/", views.account_list, name="account_list"),
    path("accounts/add/", views.add_account, name="add_account"),
    path("accounts/<int:account_id>/", views.account_detail, name="account_detail"),
    path(
        "accounts/<int:account_id>/add-transaction/",
        views.add_transaction,
        name="add_transaction",
    ),
    path("transfer/", views.transfer_money, name="transfer"),
    path("transactions/", views.transactions_list, name="transactions_list"),
    path("summary/", views.account_summary, name="summary"),
]
