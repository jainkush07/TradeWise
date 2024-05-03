# Generated by Django 3.1.7 on 2022-03-13 14:54

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employeeApp', '0027_auto_20220227_0030'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employeesalaryslips',
            name='dateForStatus',
            field=models.DateField(blank=True, default=datetime.date(2022, 3, 13), null=True),
        ),
        migrations.AlterField(
            model_name='employeesalaryslips',
            name='month',
            field=models.CharField(choices=[('January', 'January'), ('February', 'February'), ('March', 'March'), ('April', 'April'), ('May', 'May'), ('June', 'June'), ('July', 'July'), ('August', 'August'), ('September', 'September'), ('October', 'October'), ('November', 'November'), ('December', 'December')], default='March', max_length=254),
        ),
    ]
