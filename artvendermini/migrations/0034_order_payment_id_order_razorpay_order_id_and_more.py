# Generated by Django 4.2.4 on 2023-10-25 09:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('artvendermini', '0033_remove_order_payment_id_alter_order_order_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='payment_id',
            field=models.CharField(default='your_default_value_here', max_length=100),
        ),
        migrations.AddField(
            model_name='order',
            name='razorpay_order_id',
            field=models.CharField(default='your_default_value_here', max_length=100),
        ),
        migrations.AlterField(
            model_name='order',
            name='order_date',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='order',
            name='shipping_charge',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='order',
            name='total_amount',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='order',
            name='total_cost',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]