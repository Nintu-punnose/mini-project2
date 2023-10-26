# Generated by Django 4.2.4 on 2023-10-04 15:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('artvendermini', '0023_alter_userdata_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sellerprofile',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='sellerprofile',
            name='userdata',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='artvendermini.userdata'),
        ),
        migrations.AlterField(
            model_name='userdata',
            name='number',
            field=models.CharField(max_length=20),
        ),
    ]