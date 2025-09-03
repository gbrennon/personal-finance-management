# finance/admin.py
from django.contrib import admin
from .models import Transaction, Budget, Category

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'transaction_type', 'user')
    list_filter = ('transaction_type', 'user')
    search_fields = ('name',)

admin.site.register(Transaction)
admin.site.register(Budget)