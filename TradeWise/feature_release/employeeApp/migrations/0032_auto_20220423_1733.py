# Generated by Django 3.1.7 on 2022-04-23 12:03

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employeeApp', '0031_auto_20220412_1720'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employeesalaryslips',
            name='dateForStatus',
            field=models.DateField(blank=True, default=datetime.date(2022, 4, 23), null=True),
        ),
    ]
