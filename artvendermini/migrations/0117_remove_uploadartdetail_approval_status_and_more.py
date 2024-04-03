# Generated by Django 4.2.4 on 2024-03-28 05:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('artvendermini', '0116_alter_userdata_certificate'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='uploadartdetail',
            name='approval_status',
        ),
        migrations.RemoveField(
            model_name='uploadartdetail',
            name='is_approved',
        ),
        migrations.AlterField(
            model_name='userdata',
            name='certificate_status',
            field=models.CharField(choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')], default='pending', max_length=10),
        ),
    ]