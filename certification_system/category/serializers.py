from rest_framework import serializers
from .models import Category


class CategorySerializer(serializers.ModelSerializer):
    certificate_count = serializers.SerializerMethodField("get_count")

    def get_count(self, obj):
        return obj.certificates.count()

    class Meta:
        model = Category
        read_only_fields = ("created_at", "updated_at", "count")
        fields = "__all__"
