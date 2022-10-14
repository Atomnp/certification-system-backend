import uuid
from certificate.models import Certificate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import csv
import io
from io import BytesIO
from django.core.files.base import ContentFile

# Create your views here.
from rest_framework import viewsets
from rest_framework import permissions
from certificate.serializers import CertificateSerializer
from PIL import Image
from certification_system.utils.images import save_temporary_image, delete_temporary_image


def generate_certificate_dummy(template, data, mappings):
    """
    Generate certificate from template and data
    """
    file_path = save_temporary_image(template)
    image = Image.open(file_path)
    delete_temporary_image(file_path)
    image = image.convert("L")
    f = BytesIO()
    try:
        image.save(f, format="png")
        return ContentFile(f.getvalue(), name=uuid.uuid4().hex + ".png")
    finally:
        f.close()


class CertificateViewSet(viewsets.ModelViewSet):
    queryset = Certificate.objects.all().order_by("name")
    serializer_class = CertificateSerializer
    # permission_classes = [permissions.IsAuthenticated]


# route to generate bulk certificates using template image and csv file from the request
class BulkCertificateGenerator(APIView):
    def post(self, request, format=None):
        template_image = request.FILES["template_image"]
        csv_file = request.FILES["csv_file"]
        mapping = request.data["mapping"]

        file = csv_file.read().decode("utf-8")
        reader = csv.DictReader(io.StringIO(file))

        for person in reader:
            data = {
                "name": person["name"],
                "email": person["email"],
                "active": True,
                "category": request.data["category"],
                "event": request.data["event"],
                "image": generate_certificate_dummy(template_image, person, mapping),
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
            certificate.save()

        return Response(
            data={
                "success": True,
                "message": "Certificates generated successfully",
                "data": [],
            },
            status=status.HTTP_201_CREATED,
        )
