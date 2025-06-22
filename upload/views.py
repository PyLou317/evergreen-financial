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
from transactions.models import Transaction
from category.models import Category
from django.db.models import Q, Sum, Count
from django.db.models.functions import TruncMonth


# Django Forms
from django import forms
from .forms import UploadFileForm

# Django Auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

# Misc
from django.utils import formats
from .utils import categorize_transaction, add_header
from io import StringIO
from decimal import Decimal
from datetime import datetime
import csv

# Rest Framework
from rest_framework import generics, permissions, filters
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated


@login_required
def upload_statement(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)

        if form.is_valid():
            uploaded_file = form.cleaned_data['file']
            
            filename= uploaded_file.name
            print(filename)

            if 'cibc' in filename.lower():
                try:
                    file_with_header = add_header(uploaded_file)
                    file_content = file_with_header.read().decode('utf-8') 
                except NameError as e:
                    print(f'Cannot read file, error: {e}')
                except:
                    print(f'Another error has occured')
            else:
                file_content = uploaded_file.read().decode('utf-8') 
                

            csvfile =StringIO(file_content) # creates a StringIO object to process it without saving on disk
            reader = csv.DictReader(csvfile)
            
            transactions_to_create = []
            
            for row in reader:
                date_str = row.get('Date')
                description = row.get('Sub-description')
                amount_str = row.get('Amount')

                # Basic data cleaning and conversion
                if date_str:
                    try:
                        date = datetime.strptime(date_str, '%Y-%m-%d')  # Adjust format if needed
                    except ValueError:
                        print(f"Invalid date format for transaction: {description}")
                        continue

                if amount_str:
                    try:
                        amount = Decimal(amount_str.replace(',', ''))
                    except ValueError:
                        print(f"Invalid amount format for transaction: {description}")
                        continue

                # Categorize transactions
                if date and amount and description:
                    category_name = categorize_transaction(description)
                    category, created = Category.objects.get_or_create(name=category_name)

                    existing_transaction = Transaction.objects.filter(
                        date=date,
                        description=description,
                        amount=amount,
                        category=category,
                        owner=request.user
                    ).first() # Grabs the first transactions with matching values
                
                    if existing_transaction:
                        print("Duplicate transaction found, not saving.")
                    else:
                        transaction = Transaction(
                            date=date, 
                            description=description, 
                            amount=amount, 
                            category=category,
                            owner=request.user
                            )
                        transactions_to_create.append(transaction)

            Transaction.objects.bulk_create(transactions_to_create) # Bulk create transactions for efficiency
            print(f"{len(transactions_to_create)} transactions saved successfully.")

            return redirect("upload:file_upload")
    else:
        form = UploadFileForm()
    return render(request, 'upload/upload.html', {'upload_form': form})