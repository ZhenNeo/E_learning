# Generated by Django 4.1.4 on 2024-05-17 05:20

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("app", "0060_ticket"),
    ]

    operations = [
        migrations.AddField(
            model_name="course",
            name="youtube_link",
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="ticket",
            name="attachment",
            field=models.FileField(
                blank=True, null=True, upload_to="staticfiles/tickets/"
            ),
        ),
    ]