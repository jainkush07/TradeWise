# Generated by Django 3.1.7 on 2022-06-25 16:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stockApp', '0050_auto_20220612_1412'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='stockbasicdetail',
            name='startupCategory',
        ),
        migrations.AddField(
            model_name='stockbasicdetail',
            name='amount_To_Raise',
            field=models.BigIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='stockbasicdetail',
            name='daysLeft',
            field=models.BigIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='stockbasicdetail',
            name='end_Date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='stockbasicdetail',
            name='investRaisedPercent',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=100, null=True),
        ),
        migrations.AddField(
            model_name='stockbasicdetail',
            name='investment_Raised',
            field=models.BigIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='stockbasicdetail',
            name='isLaunchSoon',
            field=models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], default='No', max_length=100),
        ),
        migrations.AddField(
            model_name='stockbasicdetail',
            name='isStatusComp',
            field=models.CharField(choices=[('Completed', 'Completed'), ('Not Completed', 'Not Completed')], default='Not Completed', max_length=100),
        ),
        migrations.AddField(
            model_name='stockbasicdetail',
            name='jump_Start',
            field=models.BigIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='stockbasicdetail',
            name='launch_Date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='stockbasicdetail',
            name='launching_Soon_Type',
            field=models.CharField(blank=True, choices=[('Prebook', 'Prebook'), ('Waitlist', 'Waitlist')], max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='stockbasicdetail',
            name='shareDematerialized',
            field=models.CharField(blank=True, choices=[('Yes', 'Yes'), ('No', 'No')], max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='stockbasicdetail',
            name='type_Of_Shares',
            field=models.CharField(blank=True, choices=[('Equity', 'Equity'), ('CCPS', 'CCPS'), ('CCD', 'CCD'), ('NCD', 'NCD'), ('CSOP', 'CSOP')], max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='stockessentials',
            name='equityPercent',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=1000, null=True),
        ),
        migrations.AddField(
            model_name='stockessentials',
            name='shares_on_offer',
            field=models.BigIntegerField(blank=True, null=True),
        ),
    ]
