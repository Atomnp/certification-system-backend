from django.db import models
from category.models import Category
from event.models import Event
import uuid
from certification_system.utils.images import get_file_path

# Create your models here.
class Certificate(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()
    active = models.BooleanField()
    category = models.ForeignKey(
        Category, related_name="certificates", on_delete=models.CASCADE
    )
    event = models.ForeignKey(
        Event, related_name="certificates", on_delete=models.CASCADE
    )
    # save certificates to media/certificates folder
    image = models.ImageField(upload_to=get_file_path, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
