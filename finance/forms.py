from django import forms
from .models import Transaction
from .models import Budget

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['date', 'category', 'amount']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),}
    def __init__(self, *args, **kwargs):
        transaction_type = kwargs.pop('transaction_type', None)
        super(TransactionForm, self).__init__(*args, **kwargs)

        if transaction_type == 'Income':
            self.fields['category'].widget = forms.Select(choices=Transaction.INCOME_CATEGORIES)
        elif transaction_type == 'Expense':
            self.fields['category'].widget = forms.Select(choices=Transaction.EXPENSE_CATEGORIES)    
    

class BudgetForm(forms.ModelForm):
    class Meta:
        model = Budget
        fields = ['amount', 'month', 'year']
        widgets = {
            'month': forms.NumberInput(attrs={'min': 1, 'max': 12}),
            'year': forms.NumberInput(attrs={'min': 2000}),
        }
