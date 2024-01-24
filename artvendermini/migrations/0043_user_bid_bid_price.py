# Generated by Django 4.2.4 on 2024-01-22 04:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('artvendermini', '0042_rename_art_id_user_bid_art'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_bid',
            name='bid_price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
            preserve_default=False,
        ),
    ]
