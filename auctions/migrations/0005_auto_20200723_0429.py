# Generated by Django 3.0.8 on 2020-07-23 04:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_bid_bid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bid',
            name='bid',
        ),
        migrations.AddField(
            model_name='auction',
            name='image',
            field=models.URLField(blank=True),
        ),
    ]
