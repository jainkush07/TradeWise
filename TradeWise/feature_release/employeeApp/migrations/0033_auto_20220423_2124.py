# Generated by Django 3.1.7 on 2022-04-23 15:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employeeApp', '0032_auto_20220423_1733'),
    ]

    operations = [
        migrations.AlterField(
            model_name='country',
            name='flag',
            field=models.ImageField(blank=True, null=True, upload_to='employee/employee-profile/'),
        ),
    ]
