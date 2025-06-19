from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.urls import reverse_lazy

# Django Models
from django.db import models
from django.db.models import Sum
from transactions.models import Transaction
from category.models import Category
from django.db.models import Q, Sum, Count
from django.db.models.functions import TruncMonth

# Django Auth
from django.contrib.auth.decorators import login_required
from django.utils import timezone

# Misc
from django.utils import formats
from io import StringIO
from decimal import Decimal
from datetime import datetime
import csv

# Pagination
# from .mixins import ViewPaginatorMixin
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# from .pagination import CustomPageNumberPagination

# Serializers
from .serializers import TransactionSerializer, CategorySerializer

# Rest Framework
from rest_framework import generics, permissions, filters
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated



@login_required
def dashboard_view(request):
    expense_transactions = Transaction.objects.exclude(
        category__name='Income').filter(
            owner=request.user)
    
    expense_total_aggregation = expense_transactions.aggregate(
        total_expense_amount=Sum('amount'))
    
    today = datetime.today()
    
    # Pass months to template for drop down btn selector
    months_data = expense_transactions.annotate(
        month=TruncMonth('date')).values('month')
    month_names = []
    seen_months = set() #prevent duplicates.
    for item in months_data:
        month_date = item['month']
        month_name = month_date.strftime("%B %Y") # ex: Jan 2024
        if month_name not in seen_months:
            month_names.append((month_date, month_name))
            seen_months.add(month_name)
    
    # Custom sort function to sort by month and year
    def month_sort_key(item):
        return item[0].year, item[0].month

    month_names.sort(key=month_sort_key)
    months = [name for date, name in month_names] 
        
    income_transactions = Transaction.objects.filter(
        owner=request.user,
        category__name='Income')
    
    income_total_aggregation = income_transactions.aggregate(
        total_income_amount=Sum('amount')
     )
    
    categories = Category.objects.exclude(
            name='Income').annotate(
            total_amount=Sum('transaction__amount', filter=models.Q(
                transaction__owner=request.user))
            ).exclude(total_amount=0 or None).order_by('total_amount') #[:5]
    
    context = {
        'categories': categories,
        'income_summary': income_total_aggregation,
        'expense_summary': expense_total_aggregation,
        'months': months,
        'today': today
    }
    
    return render(request, 'dashboard/index.html', context)



# ----===== Categories API =====---- #
@login_required
def category_expenses_json(request):
    transactions = Transaction.objects.exclude(
        category__name='Income').filter(
        owner=request.user
    )

    category_expenses = transactions.values('category__name').annotate(
        total_expense=Sum('amount'),
        transaction_count=Count('id')
    ).order_by('-total_expense')
    
    # Format the data for JSON response
    category_data = []
    for item in category_expenses:        
        category_data.append({
            'category': item['category__name'], 
            'total_expense': str(item['total_expense']),
            'transaction_count': item['transaction_count']
        })
        
    return JsonResponse(category_data, safe=False)




# -----===== Income API (Graph #2) ======----- #
@login_required
def income_total_json(request):
    year = request.GET.get('year')
    if not year:
        year = 2025
        # datetime.today().year
    else:
        year = int(year)

    # Filter income transactions for the year
    income_transactions_for_year = Transaction.objects.filter(
        owner=request.user,
        date__year = year,
        category__name = 'Income'
    )
        
    # Group by month and category, and sum amounts
    monthly_income_data = income_transactions_for_year.values(
        'date__month', 'category__name'
    ).annotate(
        total_income=Sum('amount')
    ).order_by('date__month', 'category__name')
    
    
    # Format the data for JSON response
    income_data = []
    for item in monthly_income_data:
        month_number = item['date__month']
        month_name = datetime(year=year, month=month_number, day=1).strftime('%B')
        
        income_data.append({
            'month': month_name,
            'category': item['category__name'],
            'total_income': float(item['total_income'])
        })

    return JsonResponse(income_data, safe=False) # Return JSON response


# -----===== Monthly Expense API (Graph #3) =====----- #
@login_required
def monthly_expense_json(request):

    monthly_expenses = Transaction.objects.exclude(
        category__name='Income').filter(
        owner=request.user,
    ).annotate(
        month=TruncMonth('date')
    ).values('category__name', 'month').annotate(
        total_expense=Sum('amount')
    ).order_by('category__name', 'month')
    
    # Format the data for JSON response
    monthly_expense_data = []
    for item in monthly_expenses:
        monthly_expense_data.append({
            'month': item['month'].strftime('%B %Y'), 
            'category': item['category__name'],
            'total_expense': float(item['total_expense'] or 0)
        })
        
    return JsonResponse(monthly_expense_data, safe=False)