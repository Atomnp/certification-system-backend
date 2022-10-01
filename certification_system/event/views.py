from event.models import Event
from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from rest_framework import permissions
from event.serializers import EventSerializer

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all().order_by('-end_date')
    serializer_class = EventSerializer
    # permission_classes = [permissions.IsAuthenticated]
