# Generated by Django 5.1 on 2024-08-12 08:01

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="profile_picture",
            field=models.ImageField(
                blank=True, null=True, upload_to="profile_pictures/"
            ),
        ),
        migrations.AddField(
            model_name="user",
            name="profile_picture_url",
            field=models.URLField(blank=True, max_length=255, null=True),
        ),
    ]
