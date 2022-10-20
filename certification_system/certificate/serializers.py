# serializers for certificate
from rest_framework import serializers
from .models import Certificate


class CertificateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certificate
        # read only attributes
        read_only_fields = ("created_at", "updated_at")
        fields = "__all__"



