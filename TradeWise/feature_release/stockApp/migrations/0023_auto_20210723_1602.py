# Generated by Django 3.1.7 on 2021-07-23 10:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stockApp', '0022_bengrahamordcf'),
    ]

    operations = [
        migrations.AddField(
            model_name='stockadmin',
            name='metaDescriptionResearchReportListing',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='stockadmin',
            name='metaKeywordsResearchReportListing',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='stockadmin',
            name='metaTitleResearchReportListing',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='stockadmin',
            name='tagsResearchReportListing',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
    ]
