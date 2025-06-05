from django.shortcuts import render

# Django Models
from django.db import models
from django.db.models import Sum
from transactions.models import Transaction
from category.models import Category
from django.db.models import Q, Sum, Count
from django.db.models.functions import TruncMonth

# Django Auth
from django.contrib.auth.decorators import login_required

# Misc
from django.utils import formats
from .utils import categorize_transaction, add_header
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
    
    top3_categories = Category.objects.exclude(
            name='Income').annotate(
            total_amount=Sum('transaction__amount', filter=models.Q(
                transaction__owner=request.user))
            ).exclude(total_amount=0 or None).order_by('total_amount')[:5]
    
    context = {
        'categories': top3_categories,
        'income_summary': income_total_aggregation,
        'expense_summary': expense_total_aggregation,
        'months': months
    }
    
    return render(request, 'dashboard/index.html', context)