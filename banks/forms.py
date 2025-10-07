from django import forms
from .models import BankAccount, BankTransaction, BankTransfer, BankInstitution


class BankAccountForm(forms.ModelForm):
    class Meta:
        model = BankAccount
        fields = [
            "institution",
            "account_name",
            "account_type",
            "account_number",
            "current_balance",
            "available_balance",
            "credit_limit",
            "interest_rate",
            "minimum_balance",
            "monthly_fee",
            "notes",
        ]
        widgets = {
            "current_balance": forms.NumberInput(attrs={"step": "0.01"}),
            "available_balance": forms.NumberInput(attrs={"step": "0.01"}),
            "credit_limit": forms.NumberInput(attrs={"step": "0.01"}),
            "interest_rate": forms.NumberInput(attrs={"step": "0.001"}),
            "minimum_balance": forms.NumberInput(attrs={"step": "0.01"}),
            "monthly_fee": forms.NumberInput(attrs={"step": "0.01"}),
            "notes": forms.Textarea(attrs={"rows": 3}),
        }


class BankTransactionForm(forms.ModelForm):
    class Meta:
        model = BankTransaction
        fields = [
            "transaction_type",
            "amount",
            "description",
            "transaction_date",
            "category",
            "reference_number",
            "notes",
        ]
        widgets = {
            "transaction_date": forms.DateInput(attrs={"type": "date"}),
            "amount": forms.NumberInput(attrs={"step": "0.01"}),
            "notes": forms.Textarea(attrs={"rows": 3}),
        }


class BankTransferForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields["from_account"].queryset = BankAccount.objects.filter(
                user=user, is_active=True
            )
            self.fields["to_account"].queryset = BankAccount.objects.filter(
                user=user, is_active=True
            )

    class Meta:
        model = BankTransfer
        fields = [
            "from_account",
            "to_account",
            "amount",
            "transfer_date",
            "description",
            "fee",
            "notes",
        ]
        widgets = {
            "transfer_date": forms.DateInput(attrs={"type": "date"}),
            "amount": forms.NumberInput(attrs={"step": "0.01"}),
            "fee": forms.NumberInput(attrs={"step": "0.01"}),
            "notes": forms.Textarea(attrs={"rows": 3}),
        }
