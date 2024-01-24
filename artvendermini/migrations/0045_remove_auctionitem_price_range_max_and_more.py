# Generated by Django 4.2.4 on 2024-01-22 15:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('artvendermini', '0044_remove_user_bid_art_user_bid_auction_item'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='auctionitem',
            name='price_range_max',
        ),
        migrations.AddField(
            model_name='auctionitem',
            name='description',
            field=models.TextField(default=0),
            preserve_default=False,
        ),
    ]