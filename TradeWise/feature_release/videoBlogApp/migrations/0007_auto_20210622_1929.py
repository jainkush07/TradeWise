# Generated by Django 3.1.7 on 2021-06-22 13:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videoBlogApp', '0006_marketingdata_hitcountpopular'),
    ]

    operations = [
        migrations.AlterField(
            model_name='marketingdata',
            name='latestByDate',
            field=models.DateTimeField(),
        ),
    ]
