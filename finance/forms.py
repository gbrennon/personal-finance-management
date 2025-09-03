from django import forms
from .models import Transaction, Budget, Category

class TransactionForm(forms.ModelForm):
    # the category field is now a ModelChpiceField, which creates  dropdown menu
    category = forms.ModelChoiceField(queryset=Category.objects.none())

    class Meta:
        model = Transaction
        fields = ['date', 'category', 'amount']
        widgets = {
            'date' : forms.DateInput(attrs={'type': 'date'})
        }
    
    def __init__(self, *args, **kwargs):
        # Get the user and transaction_type passed from the view
        user = kwargs.pop('user', None)
        transaction_type = kwargs.pop('transaction_type', None)
        super().__init__(*args, **kwargs)

        if user and transaction_type:
            self.fields['category'].queryset = Category.objects.filter(
                user=user,
                transaction_type=transaction_type
            )    
    


class BudgetForm(forms.ModelForm):
    class Meta:
        model = Budget
        fields = ['amount', 'month', 'year']
        widgets = {
            'month': forms.NumberInput(attrs={'min': 1, 'max': 12}),
            'year': forms.NumberInput(attrs={'min': 2000}),
        }
