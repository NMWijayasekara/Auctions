# Generated by Django 3.0.8 on 2020-07-23 02:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_auction_bids_comments_watchlist'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Bids',
            new_name='Bid',
        ),
        migrations.RenameModel(
            old_name='Comments',
            new_name='Comment',
        ),
    ]
