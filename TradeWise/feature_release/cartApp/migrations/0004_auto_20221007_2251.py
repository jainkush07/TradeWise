# Generated by Django 3.1.7 on 2022-10-07 17:21

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('websiteApp', '0017_waitlistorders'),
        ('cartApp', '0003_auto_20220922_1415'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserCart',
            fields=[
                ('id', models.BigAutoField(editable=False, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('uid', models.UUIDField(default=uuid.uuid4, unique=True)),
                ('user_id', models.BigIntegerField(unique=True)),
                ('status', models.CharField(choices=[('active', 'active')], default='active', max_length=20)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='transaction',
            name='sb_Company',
            field=models.CharField(blank=True, choices=[('Planify Enterprises', 'Planify Enterprises'), ('Planify Capital', 'Planify Capital')], max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='transaction',
            name='sb_Depository',
            field=models.CharField(blank=True, choices=[('NSDL', 'NSDL'), ('CDSL', 'CDSL')], max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='transaction',
            name='sb_DpID',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='transaction',
            name='sb_ISIN',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='transaction',
            name='sb_KYC',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='transaction',
            name='sb_Quantity',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='transaction',
            name='sb_accountNo',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='transaction',
            name='sb_brokerName',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='transaction',
            name='sb_buyerBank',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='transaction',
            name='sb_buyerIdentification',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='transaction',
            name='sb_buyerName',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='transaction',
            name='sb_clientID',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='transaction',
            name='sb_company',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='transaction',
            name='sb_consideration',
            field=models.BigIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='transaction',
            name='sb_paymentReference',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='transaction',
            name='sb_resonCode',
            field=models.CharField(blank=True, choices=[('Off Market Sales', 'Off Market Sales'), ('Return Of Shares', 'Return Of Shares'), ('Internal Transfer', 'Internal Transfer')], max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='transaction',
            name='sb_shareTransfer',
            field=models.CharField(blank=True, choices=[('Initiated', 'Initiated'), ('Approved', 'Approved'), ('Transferred', 'Transferred')], max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='transaction',
            name='sb_uploadTransferRequest',
            field=models.FileField(blank=True, null=True, upload_to='investor/documents/', validators=[django.core.validators.FileExtensionValidator(['pdf', 'jpeg', 'jpg', 'png', 'bmp'])]),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='investMentPrice',
            field=models.DecimalField(decimal_places=50, default=0, max_digits=1000),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='quantity',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='txn_made_by',
            field=models.CharField(choices=[('Self', 'Self'), ('PaymentGateway', 'PaymentGateway'), ('ShareBook', 'ShareBook')], default='PaymentGateway', max_length=1000),
        ),
        migrations.CreateModel(
            name='CartItems',
            fields=[
                ('id', models.BigAutoField(editable=False, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('uid', models.UUIDField(default=uuid.uuid4, unique=True)),
                ('quantity', models.FloatField(default=0)),
                ('status', models.CharField(choices=[('active', 'active')], default='active', max_length=20)),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='CartItem', to='cartApp.usercart')),
                ('pre_ipo_stock', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='websiteApp.buypreipostocklist')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
