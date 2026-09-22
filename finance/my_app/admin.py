from django.contrib import admin
from .models import Category, Income, Expense


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(Income)
class IncomeAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'source', 'amount', 'date')
    list_filter = ('date', 'source')
    search_fields = ('user__username', 'source')


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'category',
        'amount',
        'description',
        'date'
    )

    list_filter = (
        'category',
        'date'
    )

    search_fields = (
        'user__username',
        'description'
    )