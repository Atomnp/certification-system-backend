# serializers for event
from rest_framework import serializers
from .models import Event

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        # read only attributes
        read_only_fields = ('created_at', 'updated_at')
        fields = '__all__'