from django.db import models
from event.models import Event

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    event=models.ForeignKey(Event, related_name="categories", on_delete=models.CASCADE)


    def __str__(self):
        return self.name
