# Generated by Django 5.0.4 on 2024-05-01 13:43

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0020_remove_studentassignment_marks'),
    ]

    operations = [
        migrations.CreateModel(
            name='Voucher',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(help_text='Unique code for the voucher', max_length=100, unique=True)),
                ('discount', models.DecimalField(decimal_places=2, help_text='Discount percentage or amount', max_digits=5)),
                ('expiration_date', models.DateField(help_text='Expiration date of the voucher')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Creation timestamp')),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='Last updated timestamp')),
                ('created_by', models.ForeignKey(help_text='User who created the voucher', on_delete=django.db.models.deletion.CASCADE, related_name='vouchers', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Voucher',
                'verbose_name_plural': 'Vouchers',
                'ordering': ['-created_at'],
            },
        ),
    ]
