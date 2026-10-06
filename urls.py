from django.urls import path
from . import views

urlpatterns = [
    # Auth & User APIs
    path('register/', views.register, name='register'),
    path('login/', views.login_api, name='login'),
    path('users/', views.get_all_users_api, name='get_all_users'),
    path('user/<str:username>/', views.get_user_by_username_api, name='get_user_by_username'),

    # Income APIs
    path('income/add/', views.add_income_api, name='add_income'),
    path('income/', views.get_all_income_api, name='get_all_income'),
    path('income/<int:income_id>/', views.get_income_by_id_api, name='get_income_by_id'),
    path('income/update/<int:income_id>/', views.update_income_api, name='update_income'),
    path('income/delete/<int:income_id>/', views.delete_income_api, name='delete_income'),

    # Expense APIs
    path('expense/add/', views.add_expense_api, name='add_expense'),
    path('expenses/', views.get_all_expense_api, name='get_all_expense'),
    path('expense/<int:expense_id>/', views.get_expense_by_id_api, name='get_expense_by_id'),
    path('expense/update/<int:expense_id>/', views.update_expense_api, name='update_expense'),
    path('expense/delete/<int:expense_id>/', views.delete_expense_api, name='delete_expense'),

    # Category APIs
    path('category/add/', views.add_category_api, name='add_category'),
    path('categories/', views.get_all_category_api, name='get_all_categories'),
    path('category/<int:category_id>/', views.get_category_by_id_api, name='get_category_by_id'),
    path('category/update/<int:category_id>/', views.update_category_api, name='update_category'),
    path('category/delete/<int:category_id>/', views.delete_category_api, name='delete_category'),

    # Combined Transaction History
    path('transactions/', views.get_transactions_api, name='get_transactions'),
]