# Generated by Django 3.1 on 2021-02-02 14:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('branch', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='branch',
            name='alternate_phone_number',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='branch',
            name='phone_number',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
