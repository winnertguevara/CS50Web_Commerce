# Generated by Django 4.0.1 on 2022-05-10 18:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0028_alter_listing_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='image',
            field=models.ImageField(blank=True, default='descarga.png', null=True, upload_to=''),
        ),
    ]
