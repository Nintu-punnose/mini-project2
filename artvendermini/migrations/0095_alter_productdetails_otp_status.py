# Generated by Django 4.2.4 on 2024-03-06 15:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('artvendermini', '0094_alter_productdetails_otp_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productdetails',
            name='otp_status',
            field=models.CharField(choices=[('failed', 'Failed'), ('sucess', 'Sucess')], default='failed', max_length=10),
        ),
    ]