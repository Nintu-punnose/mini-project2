# Generated by Django 4.2.4 on 2024-02-27 03:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('artvendermini', '0064_alter_deliveryprofile_pin'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deliveryprofile',
            name='pin',
            field=models.CharField(default=1, max_length=10),
            preserve_default=False,
        ),
    ]
