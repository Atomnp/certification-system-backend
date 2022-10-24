from django.db import models
from category.models import Category
from event.models import Event
import uuid
from utils.images import get_file_path

# Create your models here.
class Certificate(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50)
    email = models.EmailField()
    email_sent = models.BooleanField(default=False)
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
