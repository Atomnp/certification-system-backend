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

    # filter based on event
    def get_queryset(self):
        event_id = self.request.query_params.get("event_id", None)
        if event_id is not None:
            return self.queryset.filter(event=event_id)
        else:
            return self.queryset
