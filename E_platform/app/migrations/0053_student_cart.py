# Generated by Django 4.1.4 on 2024-05-15 16:14

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("app", "0052_delete_cart"),
    ]

    operations = [
        migrations.AddField(
            model_name="student",
            name="cart",
            field=models.ManyToManyField(blank=True, to="app.course"),
        ),
    ]
