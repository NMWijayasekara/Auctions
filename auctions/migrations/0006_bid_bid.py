# Generated by Django 3.0.8 on 2020-07-23 05:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0005_auto_20200723_0429'),
    ]

    operations = [
        migrations.AddField(
            model_name='bid',
            name='bid',
            field=models.IntegerField(default=12),
            preserve_default=False,
        ),
    ]
