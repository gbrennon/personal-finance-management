from django import forms
from django.contrib.auth.models import User
from .models import Transaction, Budget, Category, Invoice, Investment, RetirementPlan


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ["transaction_type", "amount", "category", "date"]
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),
            "amount": forms.NumberInput(attrs={"step": "0.01", "min": "0"}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        transaction_type = kwargs.pop("transaction_type", None)
        super().__init__(*args, **kwargs)

        if user and transaction_type:
            # Filter categories based on user and transaction type
            self.fields["category"].queryset = Category.objects.filter(
                user=user, transaction_type=transaction_type
            )

            # Set the transaction type field to the passed value and make it readonly
            self.fields["transaction_type"].initial = transaction_type
            self.fields["transaction_type"].widget = forms.HiddenInput()


class BudgetForm(forms.ModelForm):
    class Meta:
        model = Budget
        fields = ["amount", "month", "year"]
        widgets = {
            "amount": forms.NumberInput(attrs={"step": "0.01", "min": "0"}),
            "month": forms.Select(choices=[(i, i) for i in range(1, 13)]),
            "year": forms.NumberInput(attrs={"min": "2020", "max": "2030"}),
        }


class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = [
            "client_name",
            "client_email",
            "amount",
            "due_date",
            "description",
            "status",
        ]
        widgets = {
            "due_date": forms.DateInput(attrs={"type": "date"}),
            "amount": forms.NumberInput(attrs={"step": "0.01", "min": "0"}),
            "description": forms.Textarea(attrs={"rows": 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["client_email"].required = False
        self.fields["description"].required = False


class InvestmentForm(forms.ModelForm):
    class Meta:
        model = Investment
        fields = [
            "name",
            "investment_type",
            "amount_invested",
            "current_value",
            "expected_return_rate",
            "risk_level",
            "purchase_date",
            "notes",
        ]
        widgets = {
            "purchase_date": forms.DateInput(attrs={"type": "date"}),
            "amount_invested": forms.NumberInput(attrs={"step": "0.01", "min": "0"}),
            "current_value": forms.NumberInput(attrs={"step": "0.01", "min": "0"}),
            "expected_return_rate": forms.NumberInput(
                attrs={"step": "0.01", "min": "0", "max": "100"}
            ),
            "notes": forms.Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["current_value"].required = False
        self.fields["notes"].required = False


class RetirementPlanForm(forms.ModelForm):
    class Meta:
        model = RetirementPlan
        fields = [
            "target_retirement_amount",
            "current_age",
            "target_retirement_age",
            "monthly_contribution",
            "current_savings",
            "expected_annual_return",
        ]
        widgets = {
            "target_retirement_amount": forms.NumberInput(
                attrs={"step": "0.01", "min": "0"}
            ),
            "current_age": forms.NumberInput(attrs={"min": "18", "max": "100"}),
            "target_retirement_age": forms.NumberInput(
                attrs={"min": "50", "max": "100"}
            ),
            "monthly_contribution": forms.NumberInput(
                attrs={"step": "0.01", "min": "0"}
            ),
            "current_savings": forms.NumberInput(attrs={"step": "0.01", "min": "0"}),
            "expected_annual_return": forms.NumberInput(
                attrs={"step": "0.01", "min": "0", "max": "50"}
            ),
        }

    def clean(self):
        cleaned_data = super().clean()
        current_age = cleaned_data.get("current_age")
        target_retirement_age = cleaned_data.get("target_retirement_age")

        if current_age and target_retirement_age:
            if target_retirement_age <= current_age:
                raise forms.ValidationError(
                    "Target retirement age must be greater than current age."
                )

        return cleaned_data


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name", "transaction_type"]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        self.user = user

    def save(self, commit=True):
        category = super().save(commit=False)
        if self.user:
            category.user = self.user
        if commit:
            category.save()
        return category
