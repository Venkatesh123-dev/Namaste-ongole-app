# Generated by Django 3.1 on 2020-09-15 23:00

from django.db import migrations, models
import order.models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0003_auto_20200910_1501'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='payment_status',
            field=models.IntegerField(choices=[(0, 'CREATED'), (1, 'PAID'), (2, 'REFUND')], default=order.models.PaymentStatus['CREATED']),
        ),
        migrations.AddField(
            model_name='order',
            name='payment_type',
            field=models.IntegerField(choices=[(0, 'NONE'), (1, 'CASH_ON_DELIVERY'), (2, 'DELIVERY')], default=order.models.OrderTypes['NONE']),
        ),
    ]
