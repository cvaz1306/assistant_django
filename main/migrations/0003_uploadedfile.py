# Generated by Django 4.2.1 on 2023-09-04 18:52

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("main", "0002_message_isserver"),
    ]

    operations = [
        migrations.CreateModel(
            name="UploadedFile",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("file", models.FileField(upload_to="uploads/")),
            ],
        ),
    ]
