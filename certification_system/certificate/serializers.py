# serializers for certificate
from rest_framework import serializers
from .models import Certificate


class CertificateSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Certificate
        # read only attributes
        read_only_fields = ("created_at", "updated_at")
        fields = "__all__"

    def get_image_url(self, cert):
        request = self.context.get("request")
        image_url = cert.image.url
        return request.build_absolute_uri(image_url)
