# Generated by Django 4.1.4 on 2024-05-03 16:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("app", "0026_course_student_questionpaper_mentorship_enrollment"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="student",
            name="username",
        ),
        migrations.AddField(
            model_name="student",
            name="DOB",
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="student",
            name="EmailID",
            field=models.EmailField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name="student",
            name="Full_Name",
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name="student",
            name="Gender",
            field=models.CharField(
                choices=[("M", "Male"), ("F", "Female"), ("O", "Others")],
                default="M",
                max_length=10,
            ),
        ),
        migrations.AddField(
            model_name="student",
            name="Mobile_no",
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AddField(
            model_name="student",
            name="user",
            field=models.OneToOneField(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="enrollment",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="app.student"
            ),
        ),
        migrations.AlterField(
            model_name="mentorship",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="app.student"
            ),
        ),
        migrations.DeleteModel(
            name="Admin",
        ),
    ]
