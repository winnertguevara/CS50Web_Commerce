# Generated by Django 4.0.1 on 2022-05-05 05:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0022_remove_listing_winner'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='winner',
            field=models.IntegerField(blank=True, default=None),
        ),
    ]