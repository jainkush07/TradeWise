# Generated by Django 3.1.7 on 2021-06-24 08:21

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('videoBlogApp', '0012_auto_20210624_1313'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blogvideos',
            name='metaDescriptionVideo',
        ),
        migrations.RemoveField(
            model_name='blogvideos',
            name='metaKeywordsVideo',
        ),
        migrations.RemoveField(
            model_name='blogvideos',
            name='metaTitleVideo',
        ),
        migrations.RemoveField(
            model_name='blogvideos',
            name='tagsVideo',
        ),
        migrations.CreateModel(
            name='blogVideoDM',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('metaTitleVideo', models.CharField(blank=True, max_length=1000, null=True)),
                ('metaDescriptionVideo', models.TextField(blank=True, null=True)),
                ('metaKeywordsVideo', models.TextField(blank=True, null=True)),
                ('tagsVideo', models.CharField(blank=True, max_length=1000, null=True)),
                ('publish', models.DateTimeField(default=django.utils.timezone.now)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(choices=[('Draft', 'Draft'), ('Published', 'Published'), ('Pending For Review', 'Pending For Review'), ('Feedback Shared', 'Feedback Shared'), ('Rejected', 'Rejected')], default='Draft', max_length=50)),
                ('blogProfileName', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='blogProfileNameBVDM', to='videoBlogApp.blogvideos')),
            ],
            options={
                'verbose_name_plural': 'Blog Video DM',
            },
        ),
    ]
