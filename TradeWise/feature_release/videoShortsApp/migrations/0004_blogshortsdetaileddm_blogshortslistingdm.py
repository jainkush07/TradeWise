# Generated by Django 3.1.7 on 2021-06-25 12:18

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('videoShortsApp', '0003_delete_blogpagesectionsordering'),
    ]

    operations = [
        migrations.CreateModel(
            name='blogShortsListingDM',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('metaTitleShorts', models.CharField(blank=True, max_length=1000, null=True)),
                ('metaDescriptionShorts', models.TextField(blank=True, null=True)),
                ('metaKeywordsShorts', models.TextField(blank=True, null=True)),
                ('tagsShorts', models.CharField(blank=True, max_length=1000, null=True)),
                ('featuredImage', models.ImageField(blank=True, null=True, upload_to='blog/images')),
                ('publish', models.DateTimeField(default=django.utils.timezone.now)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(choices=[('Draft', 'Draft'), ('Published', 'Published'), ('Pending For Review', 'Pending For Review'), ('Feedback Shared', 'Feedback Shared'), ('Rejected', 'Rejected')], default='Draft', max_length=50)),
            ],
            options={
                'verbose_name_plural': 'Blog Shorts Listing DM',
            },
        ),
        migrations.CreateModel(
            name='blogShortsDetailedDM',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('metaTitleShorts', models.CharField(blank=True, max_length=1000, null=True)),
                ('metaDescriptionShorts', models.TextField(blank=True, null=True)),
                ('metaKeywordsShorts', models.TextField(blank=True, null=True)),
                ('tagsShorts', models.CharField(blank=True, max_length=1000, null=True)),
                ('featuredImage', models.ImageField(blank=True, null=True, upload_to='blog/images')),
                ('publish', models.DateTimeField(default=django.utils.timezone.now)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(choices=[('Draft', 'Draft'), ('Published', 'Published'), ('Pending For Review', 'Pending For Review'), ('Feedback Shared', 'Feedback Shared'), ('Rejected', 'Rejected')], default='Draft', max_length=50)),
                ('blogProfileName', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='blogProfileNameBNDDM', to='videoShortsApp.blogvideosshorts')),
            ],
            options={
                'verbose_name_plural': 'Blog Shorts Detailed DM',
            },
        ),
    ]
