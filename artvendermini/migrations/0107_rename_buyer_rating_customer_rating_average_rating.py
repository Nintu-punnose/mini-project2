# Generated by Django 4.2.4 on 2024-03-18 04:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('artvendermini', '0106_rating'),
    ]

    operations = [
        migrations.RenameField(
            model_name='rating',
            old_name='buyer',
            new_name='customer',
        ),
        migrations.AddField(
            model_name='rating',
            name='average_rating',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]