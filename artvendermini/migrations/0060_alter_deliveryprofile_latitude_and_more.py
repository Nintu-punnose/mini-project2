# Generated by Django 4.2.4 on 2024-02-27 03:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('artvendermini', '0059_alter_deliveryprofile_latitude_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deliveryprofile',
            name='latitude',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='deliveryprofile',
            name='longitude',
            field=models.CharField(max_length=255, null=True),
        ),
    ]