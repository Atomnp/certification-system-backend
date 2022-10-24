from certificate.models import Certificate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import csv
import io
from collections import namedtuple
from event.models import Event
from category.models import Category
from utils.email import send_bulk_email


# Create your views here.
from rest_framework import viewsets
from rest_framework import permissions
from certificate.serializers import CertificateSerializer
from utils.text_injection import (
    generate_certificate,
    extract_placeholders,
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


class EmailSenderView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, format=None):
        """
        if event id is in the request send mail to all the certificates of that event
        else if request has category send mail to all the certificates of that category
        finally is we want to send email for only one certificate the request should contain only certificate id
        """
        # send email to each certificate
        send_all = request.data.get("send_all", False)
        event_id = request.data.get("event", None)
        category_id = request.data.get("category", None)
        certificate_id = request.data.get("certificate", None)
        # template = request.FILES["template_file"].read().decode("utf-8")
        # subject = request.data["subject"]
        certificates = None
        if event_id:
            event = Event.objects.get(id=int(event_id))
            certificates = event.certificates.all()
        elif category_id:
            category = Category.objects.get(id=category_id)
            certificates = category.certificates.all()
        else:
            certificate = Certificate.objects.get(pk=certificate_id)
            certificates = [certificate]

        fail_count, success_count = send_bulk_email(
            certificates, filter_already_sent=not send_all
        )
        return Response(
            data={
                "message": f"Emails sent successfully {fail_count} failed, {success_count} success",
                "falied_count": fail_count,
                "success_count": success_count,
            },
            status=status.HTTP_200_OK,
        )
