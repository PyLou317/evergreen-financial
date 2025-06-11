from django.urls import path

from .views import *

app_name = 'transactions'

urlpatterns = [
    path('', TransactionListView.as_view(), name='transactions'),
    path('<int:pk>/update/', TransactionUpdateView.as_view(), name='edit_transaction'),
    path('<int:pk>/delete/', TransactionDeleteView.as_view(), name='delete_transaction'),
    
    # API's
    path('transactions_api/', TransactionListAPIView.as_view(), name='transactions_api'),
]