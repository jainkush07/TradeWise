# Generated by Django 3.1.7 on 2022-08-04 17:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('investorApp', '0003_auto_20220621_2226'),
    ]

    operations = [
        migrations.AddField(
            model_name='investorbankdetails',
            name='bankVerified',
            field=models.CharField(blank=True, choices=[('Yes', 'Yes'), ('No', 'No')], max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='investorbankdetails',
            name='upiID',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='investordmatdetails',
            name='dmatVerified',
            field=models.CharField(blank=True, choices=[('Yes', 'Yes'), ('No', 'No')], max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='investorpersonaldetails',
            name='aadharVerified',
            field=models.CharField(blank=True, choices=[('Yes', 'Yes'), ('No', 'No')], max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='investorpersonaldetails',
            name='emailVerified',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AddField(
            model_name='investorpersonaldetails',
            name='panVerified',
            field=models.CharField(blank=True, choices=[('Yes', 'Yes'), ('No', 'No')], max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='investorpersonaldetails',
            name='personalDetailVerified',
            field=models.CharField(blank=True, choices=[('Yes', 'Yes'), ('No', 'No')], max_length=100, null=True),
        ),
        migrations.CreateModel(
            name='verificationStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('aadharVerifiedStatus', models.CharField(blank=True, choices=[('Yes', 'Yes'), ('No', 'No')], max_length=100, null=True)),
                ('panVerifiedStatus', models.CharField(blank=True, choices=[('Yes', 'Yes'), ('No', 'No')], max_length=100, null=True)),
                ('personalDetailVerifiedStatus', models.CharField(blank=True, choices=[('Yes', 'Yes'), ('No', 'No')], max_length=100, null=True)),
                ('bankVerifiedStatus', models.CharField(blank=True, default='Empty', max_length=100, null=True)),
                ('dmatVerifiedStatus', models.CharField(blank=True, default='Empty', max_length=100, null=True)),
                ('getVerifiedProgress', models.IntegerField(blank=True, null=True)),
                ('getPersonalStatus', models.CharField(blank=True, default='Filled', max_length=100, null=True)),
                ('getAadharStatus', models.CharField(blank=True, default='Empty', max_length=100, null=True)),
                ('getPanStatus', models.CharField(blank=True, default='Empty', max_length=100, null=True)),
                ('publish', models.DateTimeField(default=django.utils.timezone.now)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(choices=[('draft', 'Draft'), ('published', 'Published')], default='draft', max_length=10)),
                ('profileOwner', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profileOwnerVSD', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Investor Verification Status',
            },
        ),
    ]
