from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.urls import reverse_lazy

# Django Views
from django.views.generic import TemplateView, View
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView, DeleteView


# Django Models
from django.db import models
from django.db.models import Sum, Min, Max
from .models import Transaction, Category
from django.db.models import Q, Sum, Count
from django.db.models.functions import TruncMonth


# Django Forms
from django import forms

# Django Auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

# Misc
from django.utils import formats
from io import StringIO
from decimal import Decimal
from datetime import datetime
import csv

# Pagination
from .mixins import ViewPaginatorMixin
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .pagination import CustomPageNumberPagination

# Serializers
from .serializers import TransactionSerializer

# Rest Framework
from rest_framework import generics, permissions, filters
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated

# Create your views here.

class TransactionListView(LoginRequiredMixin, ListView):
    template_name = 'finance_tracker/transaction_list.html'
    model = Transaction
    context_object_name = 'transactions'



class TransactionListAPIView(generics.ListCreateAPIView):
    serializer_class = TransactionSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPageNumberPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['description', 'amount', 'date', 'category__name']
    
    def get_queryset(self):
        queryset = Transaction.objects.filter(owner=self.request.user).exclude(category__name='Income')
        category = self.request.query_params.get('category')
        
        if category:
                queryset = queryset.filter(category__name=category)
                
        return queryset.order_by('-date')
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        total_transactions = queryset.count()
        total_amount = queryset.aggregate(Sum('amount'))['amount__sum'] or 0
        min_date = queryset.aggregate(Min('date'))
        max_date = queryset.aggregate(Max('date'))
        
        categories = Transaction.objects.filter(
            owner=request.user).values_list(
                'category__name', flat=True).distinct().order_by('category__name')
        
        formatted_min_date = min_date['date__min'].strftime("%b %d, %Y") if 'date__min' in min_date and min_date['date__min'] else 'N/A'
        formatted_max_date = max_date['date__max'].strftime("%b %d, %Y") if 'date__max' in max_date and max_date['date__max'] else 'N/A'

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            response_data = {
                'next': self.paginator.get_next_link(),
                'previous': self.paginator.get_previous_link(),
                'current_page': self.paginator.page.number,
                'total_pages': self.paginator.page.paginator.num_pages,
                'categories': categories,
                'stats': {
                    'min_date': formatted_min_date,
                    'max_date': formatted_max_date,
                    'total_transactions': total_transactions,
                    'total_amount': total_amount,
                },
                'results': serializer.data
            }
            return Response(response_data)

        serializer = self.get_serializer(queryset, many=True)
        response_data = {
            'stats': {
                'min_date': formatted_min_date,
                'max_date': formatted_max_date,
                'total_transactions': total_transactions,
                'total_amount': total_amount,  
            },
            'results': serializer.data,
        }
        return Response(response_data)


    def perform_create(self, serializer):
        """Override to set the owner of the transaction to the current user."""
        serializer.save(owner=self.request.user)