from certificate.models import Certificate
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.exceptions import APIException
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
    """Threre are two positioning methods auto_detect and manual.

    In auto_detect:
        1. The template image contains the placeholders which are to be replaced with the data from the csv file.
        2. The placeholders positions are extracted and then placeholders are  removed from the image.
        3. Mapping file should contain (column_name, placeholder_text,alignment,fontsize)

    In manual:
        1. The template image does not contain any placeholders.
        2. The mapping file should contain (column_name, posx, posy,alignment,fontsize)
    """

    def post(self, request, format=None):
        template_image = request.FILES["template_image"]
        csv_file = request.FILES["csv_file"]
        mapping_file = request.FILES["mapping"]
        positioning_method = request.data["positioning_method"]  # auto detect , manual

        lines = mapping_file.read().decode("utf-8").splitlines()
        AutoDetectMappingType = namedtuple(
            "Mapping", "csv_column placeholder alignment font_size"
        )
        ManualDetectMappingType = namedtuple(
            "Mapping", "csv_column posx posy alignment font_size"
        )
        try:
            mapping = (
                [AutoDetectMappingType(*line.split(",")) for line in lines]
                if positioning_method == "auto_detect"
                else [ManualDetectMappingType(*line.split(",")) for line in lines]
            )
        except Exception as e:
            raise ValidationError(
                "Mapping file should be in te format column_name, placeholder_text,alignment,fontsize"
            )

        given_placeholders = [m[1] for m in mapping]

        # converting csv file to dictionary
        file = csv_file.read().decode("utf-8")
        reader = csv.DictReader(io.StringIO(file))

        # check if the csv file has the required columns
        required_fields = ["Name", "Email"]
        for m in required_fields:
            if m not in reader.fieldnames:
                raise ValidationError(
                    f"CSV file does not contain the column {m.csv_column}"
                )

        image = Image.open(template_image)
        extracted_placeholders = []
        if positioning_method == "auto_detect":
            # extracting placeholders and removing placeholders from image
            extracted_placeholders = extract_placeholders(
                image, placeholders_text=given_placeholders
            )

            image = remove_text_from_image(image, extracted_placeholders.keys())

        certificates = []
        for person in reader:
            from_csv = {k.lower(): person[k] for k in required_fields}
            data = {
                **from_csv,
                "active": True,
                "category": request.data["category"],
                "event": request.data["event"],
                "image": generate_certificate(
                    image=image,
                    person=person,
                    mapping=mapping,
                    placeholders=extracted_placeholders,
                    positioning_method=positioning_method,
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


class TestTemplate(APIView):
    def post(self, request, format=None):
        template_image = request.FILES["template_image"]
        mapping_file = request.FILES["mapping"]

        lines = mapping_file.read().decode("utf-8").splitlines()
        MappingType = namedtuple(
            "Mapping", "csv_column placeholder alignment font_size"
        )
        mapping = [MappingType(*line.split(",")) for line in lines]

        prefixes = [m[1] for m in mapping]

        image = Image.open(template_image)

        placeholders = extract_placeholders(image, prefixes=prefixes)

        print(placeholders)
        return Response(
            data=placeholders,
            status=status.HTTP_201_CREATED,
        )


# view to directly send html response for social share
class DetailFromImageId(APIView):
    permission_classes = [AllowAny]

    def get(self, request, image_id):
        cer = None
        try:
            cer = Certificate.objects.get(image="certificates/" + image_id + ".png")
        except Exception as e:
            raise APIException()

        return Response(
            data={
                "name": cer.name,
                "event": cer.event.name,
                "category": cer.category.name,
            }
        )
