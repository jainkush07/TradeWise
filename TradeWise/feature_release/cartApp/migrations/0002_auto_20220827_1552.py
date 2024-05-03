# Generated by Django 3.1.7 on 2022-08-27 10:22

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('stockApp', '0055_auto_20220820_2239'),
        ('cartApp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='transaction',
            name='investMentPrice',
            field=models.DecimalField(blank=True, decimal_places=50, max_digits=1000, null=True),
        ),
        migrations.AddField(
            model_name='transaction',
            name='publish',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='transaction',
            name='quantity',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='transaction',
            name='status',
            field=models.CharField(choices=[('draft', 'Draft'), ('published', 'Published')], default='draft', max_length=10),
        ),
        migrations.AddField(
            model_name='transaction',
            name='trxnDate',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='transaction',
            name='txn_made_by',
            field=models.CharField(choices=[('Self', 'Self'), ('PaymentGateway', 'PaymentGateway')], default='PaymentGateway', max_length=1000),
        ),
        migrations.AddField(
            model_name='transaction',
            name='updated',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='amount',
            field=models.DecimalField(blank=True, decimal_places=50, max_digits=1000, null=True),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='selected_stock',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='transactionStock', to='stockApp.stockbasicdetail'),
        ),
    ]
