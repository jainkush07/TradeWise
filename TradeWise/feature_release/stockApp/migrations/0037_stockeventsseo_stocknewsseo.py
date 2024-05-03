# Generated by Django 3.1.7 on 2021-11-09 08:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('stockApp', '0036_auto_20211109_1328'),
    ]

    operations = [
        migrations.CreateModel(
            name='stockNewsSEO',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('newsDescriptionSEO', models.TextField(blank=True, null=True)),
                ('publish', models.DateTimeField(default=django.utils.timezone.now)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(choices=[('draft', 'Draft'), ('published', 'Published')], default='draft', max_length=10)),
                ('analyst', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='analystStockNewsSEO', to=settings.AUTH_USER_MODEL)),
                ('stockProfileName', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='stockProfileNameStockNewsSEO', to='stockApp.stockbasicdetail')),
                ('verifiedBy', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='verifiedByStockNewsSEO', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Stock News SEO - Description',
            },
        ),
        migrations.CreateModel(
            name='stockEventsSEO',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('eventsDescriptionSEO', models.TextField(blank=True, null=True)),
                ('publish', models.DateTimeField(default=django.utils.timezone.now)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(choices=[('draft', 'Draft'), ('published', 'Published')], default='draft', max_length=10)),
                ('analyst', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='analystStockEventsSEO', to=settings.AUTH_USER_MODEL)),
                ('stockProfileName', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='stockProfileNameStockEventsSEO', to='stockApp.stockbasicdetail')),
                ('verifiedBy', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='verifiedByStockEventsSEO', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Stock Events SEO - Description',
            },
        ),
    ]
