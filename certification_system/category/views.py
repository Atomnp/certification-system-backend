from category.models import Category
from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from rest_framework import permissions
from category.serializers import CategorySerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    # permission_classes = [permissions.IsAuthenticated]

