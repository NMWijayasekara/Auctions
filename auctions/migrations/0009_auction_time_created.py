# Generated by Django 3.0.8 on 2020-07-29 01:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0008_auto_20200723_1459'),
    ]

    operations = [
        migrations.AddField(
            model_name='auction',
            name='time_created',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
