# Generated by Django 4.2.4 on 2023-09-30 08:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('artvendermini', '0019_producttype'),
    ]

    operations = [
        migrations.RenameField(
            model_name='producttype',
            old_name='name',
            new_name='nametype',
        ),
    ]
