# Generated by Django 4.2.4 on 2024-01-19 06:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('artvendermini', '0038_auctionitem_is_active'),
    ]

    operations = [
        migrations.CreateModel(
            name='User_Bid',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('starting_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('bid_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('ending_time', models.DateTimeField()),
                ('buyer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='buyer_auctions', to=settings.AUTH_USER_MODEL)),
                ('seller', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='seller_auctions', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
