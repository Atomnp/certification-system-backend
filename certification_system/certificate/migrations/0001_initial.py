# Generated by Django 4.1.1 on 2022-10-24 07:54

from django.db import migrations, models
import django.db.models.deletion
import utils.images
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("category", "0001_initial"),
        ("event", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Certificate",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.UUID("0876b06d-cfa1-45c8-9c91-3c6c1c7d7965"),
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("name", models.CharField(max_length=50)),
                ("email", models.EmailField(max_length=254)),
                ("active", models.BooleanField()),
                (
                    "image",
                    models.ImageField(
                        blank=True, null=True, upload_to=utils.images.get_file_path
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "category",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="certificates",
                        to="category.category",
                    ),
                ),
                (
                    "event",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="certificates",
                        to="event.event",
                    ),
                ),
            ],
        ),
    ]
