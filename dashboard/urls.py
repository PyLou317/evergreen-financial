from django.urls import path

from .views import *

app_name = 'dashboard'

urlpatterns = [
    path('', dashboard_view, name='dashboard_home'),
    
    # API's
    path('category_expense_json/', category_expenses_json, name='category_expense_json'),
    path('monthly_expense_json/', monthly_expense_json, name='monthly_expense_json'),
    path('income_total_json/', income_total_json, name='income_total_json'),
    
]