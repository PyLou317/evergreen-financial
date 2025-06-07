from django.urls import path

from .views import *

app_name = 'transactions'

urlpatterns = [
    path('transactions/', TransactionListView.as_view(), name='transactions'),
    
    # API's
    path('transactions_api/', TransactionListAPIView.as_view(), name='transactions_api'),
]