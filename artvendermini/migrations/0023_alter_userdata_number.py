# Generated by Django 4.2.4 on 2023-10-01 12:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('artvendermini', '0022_alter_userdata_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdata',
            name='number',
            field=models.CharField(default='default_value_here', max_length=20),
        ),
    ]