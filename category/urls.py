from django.urls import path

from .views import *

app_name = 'category'

urlpatterns = [
    path('categories/', CategoryList.as_view(), name='categories'),
    
    # API's
    path('categories-api', CategoryListAPIView.as_view(), name='categories-api'),
]