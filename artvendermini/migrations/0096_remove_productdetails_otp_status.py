# Generated by Django 4.2.4 on 2024-03-06 15:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('artvendermini', '0095_alter_productdetails_otp_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productdetails',
            name='otp_status',
        ),
    ]