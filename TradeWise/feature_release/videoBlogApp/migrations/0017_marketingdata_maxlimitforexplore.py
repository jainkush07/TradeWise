# Generated by Django 3.1.7 on 2021-06-30 17:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videoBlogApp', '0016_videosheadingdm'),
    ]

    operations = [
        migrations.AddField(
            model_name='marketingdata',
            name='maxLimitForExplore',
            field=models.PositiveIntegerField(default=1),
            preserve_default=False,
        ),
    ]
