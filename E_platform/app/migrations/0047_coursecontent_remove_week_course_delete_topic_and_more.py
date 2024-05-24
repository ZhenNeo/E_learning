# Generated by Django 4.1.4 on 2024-05-10 13:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("app", "0046_course_duration_in_weeks_week_topic"),
    ]

    operations = [
        migrations.CreateModel(
            name="CourseContent",
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
                ("week_number", models.PositiveIntegerField()),
                ("topic_title", models.CharField(max_length=100)),
                (
                    "topic_video",
                    models.FileField(
                        blank=True, null=True, upload_to="staticfiles/topic_videos/"
                    ),
                ),
                (
                    "course",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="contents",
                        to="app.course",
                    ),
                ),
            ],
        ),
        migrations.RemoveField(
            model_name="week",
            name="course",
        ),
        migrations.DeleteModel(
            name="Topic",
        ),
        migrations.DeleteModel(
            name="Week",
        ),
    ]
