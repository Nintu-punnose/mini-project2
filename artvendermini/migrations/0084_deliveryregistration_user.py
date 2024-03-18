# Generated by Django 4.2.4 on 2024-03-04 18:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('artvendermini', '0083_deliveryregistration_approval_status_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='deliveryregistration',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]