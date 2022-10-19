from certificate.models import Certificate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import csv
import io
import json

# Create your views here.
from rest_framework import viewsets
from rest_framework import permissions
from certificate.serializers import CertificateSerializer
from utils.text_injection import remove_text_from_image
from utils.text_injection import generate_certificate
from utils.text_injection import extract_placeholders
from utils.text_injection import save_temporary_image
from PIL import Image


class CertificateViewSet(viewsets.ModelViewSet):
    queryset = Certificate.objects.all().order_by("name")
    serializer_class = CertificateSerializer
    # permission_classes = [permissions.IsAuthenticated]


# route to generate bulk certificates using template image and csv file from the request
class BulkCertificateGenerator(APIView):
    def post(self, request, format=None):
        template_image = request.FILES["template_image"]
        csv_file = request.FILES["csv_file"]
        mapping_file = request.FILES["mapping"]

        # converting mapping text file into dictionary

        mapping = mapping_file.read().decode("utf-8")
        mapping = mapping.split('\r\n')
        
        map_dict = {}
        
        for line in mapping:
            listDetails = line.strip().split(',')
            
            map_dict[listDetails[0]] = ({"placeholder": listDetails[1]})
            map_dict[listDetails[0]].update({"alignment": listDetails[2]})
            
        
        #converting csv file to dictionary

        file = csv_file.read().decode("utf-8")
        reader = csv.DictReader(io.StringIO(file))


        file_path = save_temporary_image(template_image)
        image = Image.open(file_path)
        #delete_temporary_image(file_path)

        #extracting placeholders and removing placeholders from image 
        placeholders = extract_placeholders(image)
        image = remove_text_from_image(image, placeholders.keys())
        
        
        for person in reader:
            data = {
                "name": person["name"],
                "email": person["email"],
                "active": True,
                "category": request.data["category"],
                "event": request.data["event"],
                "image": generate_certificate(image = image,person = person, map_dict = map_dict,placeholders=placeholders),
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
