# Generated by Django 3.1.7 on 2022-05-22 16:48

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employeeApp', '0038_auto_20220514_2330'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employeesalaryslips',
            name='dateForStatus',
            field=models.DateField(blank=True, default=datetime.date(2022, 5, 22), null=True),
        ),
    ]
