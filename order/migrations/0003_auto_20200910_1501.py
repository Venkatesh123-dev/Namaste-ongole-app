# Generated by Django 3.1 on 2020-09-10 09:31

from django.db import migrations
import order.fields


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0002_auto_20200910_1453'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='gateway_order_response',
            field=order.fields.JSONField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='payment',
            name='payment_response',
            field=order.fields.JSONField(blank=True, null=True),
        ),
    ]
