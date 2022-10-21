from certificate.models import Certificate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import csv
import io
import json
from collections import namedtuple

# Create your views here.
from rest_framework import viewsets
from rest_framework import permissions
from certificate.serializers import CertificateSerializer
from utils.text_injection import (
    generate_certificate,
    extract_placeholders,
    save_temporary_image,
    delete_temporary_image,
    remove_text_from_image,
)


from PIL import Image


class CertificateViewSet(viewsets.ModelViewSet):
    queryset = Certificate.objects.all().order_by("name")
    serializer_class = CertificateSerializer
    # permission_classes = [permissions.IsAuthenticated]

    # filter based on category
    def get_queryset(self):
        category_id = self.request.query_params.get("category", None)
        if category_id is not None:
            return self.queryset.filter(category=category_id)
        else:
            return self.queryset


# route to generate bulk certificates using template image and csv file from the request
class BulkCertificateGenerator(APIView):
    def post(self, request, format=None):
        template_image = request.FILES["template_image"]
        csv_file = request.FILES["csv_file"]
        mapping_file = request.FILES["mapping"]

        lines = mapping_file.read().decode("utf-8").splitlines()
        MappingType = namedtuple(
            "Mapping", "csv_column placeholder alignment font_size"
        )
        mapping = [MappingType(*line.split(",")) for line in lines]

        # converting csv file to dictionary

        file = csv_file.read().decode("utf-8")
        reader = csv.DictReader(io.StringIO(file))

        image = Image.open(template_image)

        # extracting placeholders and removing placeholders from image
        placeholders = extract_placeholders(image)
        image = remove_text_from_image(image, placeholders.keys())

        certificates = []
        for person in reader:
            data = {
                "name": person["name"],
                "email": person["email"],
                "active": True,
                "category": request.data["category"],
                "event": request.data["event"],
                "image": generate_certificate(
                    image=image,
                    person=person,
                    mapping=mapping,
                    placeholders=placeholders,
                ),
            }

            certificate = CertificateSerializer(data=data)
            try:
                certificate.is_valid(raise_exception=True)
            except Exception as e:
                print(e)
                return Response(
                    {"error": "Invalid data", "message": str(e)},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            cert = certificate.save()
            certificates.append(
                CertificateSerializer(cert, context={"request": request}).data
            )
        return Response(
            data=certificates,
            status=status.HTTP_201_CREATED,
        )
