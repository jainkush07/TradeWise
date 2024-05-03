# Generated by Django 3.1.7 on 2021-06-17 07:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('stockApp', '0016_auto_20210527_1527'),
    ]

    operations = [
        migrations.CreateModel(
            name='foundingRoundsFigureUnits',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('foundingUnitNumbers', models.CharField(blank=True, choices=[('K', 'K'), ('L', 'L'), ('Cr', 'Cr'), ('M', 'M')], default='Cr', max_length=10, null=True)),
                ('publish', models.DateTimeField(default=django.utils.timezone.now)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(choices=[('draft', 'Draft'), ('published', 'Published')], default='draft', max_length=10)),
                ('analyst', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='JanalystFFU', to=settings.AUTH_USER_MODEL)),
                ('stockProfileName', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='JstockProfileNameFFU', to='stockApp.stockbasicdetail')),
                ('verifiedBy', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='JverifiedByFFU', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Funding Units Numbers - Data Units(cr/lakh.. etc)',
            },
        ),
    ]
