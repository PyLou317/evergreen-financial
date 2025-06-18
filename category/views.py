from django.shortcuts import render

from .models import *
from dashboard.serializers import CategorySerializer

from django.views.generic.list import ListView

# Django Auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

# Rest Framework
from rest_framework import generics, permissions, filters
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated



class CategoryList(LoginRequiredMixin, ListView):
    template_name = 'category/category_list.html'
    model = Category
    context_object_name = 'categories'
    
    
# ----===== Category DRF ListView API =====---- #
class CategoryListAPIView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]