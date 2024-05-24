# Generated by Django 5.0.4 on 2024-04-30 13:54

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0013_remove_course_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='category',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='app.category', verbose_name='Category'),
            preserve_default=False,
        ),
    ]
