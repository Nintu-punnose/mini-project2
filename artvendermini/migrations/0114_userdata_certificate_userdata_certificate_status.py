# Generated by Django 4.2.4 on 2024-03-20 04:45

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('artvendermini', '0113_remove_userdata_certificate_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='userdata',
            name='certificate',
            field=models.FileField(blank=True, upload_to='admin_certificates/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['pdf'])]),
        ),
        migrations.AddField(
            model_name='userdata',
            name='certificate_status',
            field=models.CharField(choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')], default='approved', max_length=10),
        ),
    ]
