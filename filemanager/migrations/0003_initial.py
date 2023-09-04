# Generated by Django 4.2.1 on 2023-09-04 19:06

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("filemanager", "0002_delete_uploadedfile"),
    ]

    operations = [
        migrations.CreateModel(
            name="File",
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
                ("file", models.FileField(upload_to="")),
                ("name", models.TextField(max_length=50)),
            ],
        ),
    ]
