# Generated by Django 4.2.4 on 2024-02-28 06:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('artvendermini', '0073_remove_auctionorder_auction_listing_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='auctionorder',
            name='auction_item',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, to='artvendermini.auctionlisting'),
            preserve_default=False,
        ),
    ]
