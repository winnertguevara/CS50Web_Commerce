# Generated by Django 4.0.1 on 2022-05-05 05:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0019_listing_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='winner',
            field=models.IntegerField(blank=True, default=None),
            preserve_default=False,
        ),
    ]
