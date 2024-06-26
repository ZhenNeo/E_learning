# Generated by Django 4.1.4 on 2024-05-15 17:12

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("app", "0057_remove_course_timestamp"),
    ]

    operations = [
        migrations.AlterField(
            model_name="course",
            name="this_course_includes",
            field=models.TextField(
                blank=True, null=True, verbose_name="This Course Includes"
            ),
        ),
        migrations.AlterField(
            model_name="course",
            name="what_you_will_learn",
            field=models.TextField(
                blank=True, null=True, verbose_name="What You Will Learn"
            ),
        ),
    ]
