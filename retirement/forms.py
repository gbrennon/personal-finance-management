from django import forms
from .models import RetirementAccount, RetirementContribution, RetirementGoal


class RetirementAccountForm(forms.ModelForm):
    class Meta:
        model = RetirementAccount
        fields = [
            "account_name",
            "account_type",
            "provider",
            "account_number",
            "current_balance",
            "employer_match_rate",
            "vesting_schedule",
        ]
        widgets = {
            "current_balance": forms.NumberInput(attrs={"step": "0.01"}),
            "employer_match_rate": forms.NumberInput(attrs={"step": "0.01"}),
            "vesting_schedule": forms.Textarea(attrs={"rows": 3}),
        }


class RetirementContributionForm(forms.ModelForm):
    class Meta:
        model = RetirementContribution
        fields = [
            "contribution_type",
            "amount",
            "contribution_date",
            "tax_year",
            "notes",
        ]
        widgets = {
            "contribution_date": forms.DateInput(attrs={"type": "date"}),
            "amount": forms.NumberInput(attrs={"step": "0.01"}),
            "notes": forms.Textarea(attrs={"rows": 3}),
        }


class RetirementGoalForm(forms.ModelForm):
    class Meta:
        model = RetirementGoal
        fields = [
            "target_retirement_age",
            "target_retirement_amount",
            "current_age",
            "annual_income",
            "expected_annual_return",
            "inflation_rate",
            "retirement_income_replacement",
        ]
        widgets = {
            "target_retirement_amount": forms.NumberInput(attrs={"step": "0.01"}),
            "annual_income": forms.NumberInput(attrs={"step": "0.01"}),
            "expected_annual_return": forms.NumberInput(attrs={"step": "0.01"}),
            "inflation_rate": forms.NumberInput(attrs={"step": "0.01"}),
            "retirement_income_replacement": forms.NumberInput(attrs={"step": "0.01"}),
        }
