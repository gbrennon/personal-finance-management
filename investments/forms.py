from django import forms
from .models import Investment, InvestmentType, InvestmentTransaction


class InvestmentForm(forms.ModelForm):
    class Meta:
        model = Investment
        fields = [
            "name",
            "symbol",
            "investment_type",
            "purchase_date",
            "purchase_price",
            "quantity",
            "current_price",
            "notes",
        ]
        widgets = {
            "purchase_date": forms.DateInput(attrs={"type": "date"}),
            "purchase_price": forms.NumberInput(attrs={"step": "0.01"}),
            "quantity": forms.NumberInput(attrs={"step": "0.000001"}),
            "current_price": forms.NumberInput(attrs={"step": "0.01"}),
            "notes": forms.Textarea(attrs={"rows": 3}),
        }


class InvestmentTransactionForm(forms.ModelForm):
    class Meta:
        model = InvestmentTransaction
        fields = [
            "transaction_type",
            "quantity",
            "price_per_unit",
            "transaction_date",
            "fees",
            "notes",
        ]
        widgets = {
            "transaction_date": forms.DateInput(attrs={"type": "date"}),
            "quantity": forms.NumberInput(attrs={"step": "0.000001"}),
            "price_per_unit": forms.NumberInput(attrs={"step": "0.01"}),
            "fees": forms.NumberInput(attrs={"step": "0.01"}),
            "notes": forms.Textarea(attrs={"rows": 3}),
        }
