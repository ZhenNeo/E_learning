# Generated by Django 5.0.4 on 2024-04-25 09:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_alter_admin_emailid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='admin',
            name='DOB',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='admin',
            name='EmailID',
            field=models.EmailField(default=1, max_length=255),
            preserve_default=False,
        ),
    ]