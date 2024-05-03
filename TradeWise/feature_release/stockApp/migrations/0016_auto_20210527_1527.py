# Generated by Django 3.1.7 on 2021-05-27 15:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stockApp', '0015_stockessentials_essentialsdescription'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='stockadmin',
            name='metaDescriptionFinancial',
        ),
        migrations.RemoveField(
            model_name='stockadmin',
            name='metaKeywordsFinancial',
        ),
        migrations.RemoveField(
            model_name='stockadmin',
            name='metaTitleFinancial',
        ),
        migrations.RemoveField(
            model_name='stockadmin',
            name='tagsFinancial',
        ),
        migrations.AddField(
            model_name='stockadmin',
            name='metaDescriptionFinancialBalanceSheet',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='stockadmin',
            name='metaDescriptionFinancialCashFlow',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='stockadmin',
            name='metaDescriptionFinancialProfitLoss',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='stockadmin',
            name='metaKeywordsFinancialBalanceSheet',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='stockadmin',
            name='metaKeywordsFinancialCashFlow',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='stockadmin',
            name='metaKeywordsFinancialProfitLoss',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='stockadmin',
            name='metaTitleFinancialBalanceSheet',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='stockadmin',
            name='metaTitleFinancialCashFlow',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='stockadmin',
            name='metaTitleFinancialProfitLoss',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='stockadmin',
            name='tagsFinancialBalanceSheet',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='stockadmin',
            name='tagsFinancialCashFlow',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='stockadmin',
            name='tagsFinancialProfitLoss',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
    ]
