# Generated by Django 3.1.7 on 2021-07-23 15:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mediaBlogApp', '0004_mediablogdm'),
    ]

    operations = [
        migrations.AddField(
            model_name='mediablogdm',
            name='metaFeaturedImage',
            field=models.ImageField(blank=True, null=True, upload_to='media/images/featured'),
        ),
    ]
