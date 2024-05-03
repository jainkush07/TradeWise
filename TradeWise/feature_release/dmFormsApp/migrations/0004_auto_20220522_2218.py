# Generated by Django 3.1.7 on 2022-05-22 16:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dmFormsApp', '0003_auto_20220423_2124'),
    ]

    operations = [
        migrations.AlterField(
            model_name='metadetailfordm',
            name='static_page',
            field=models.CharField(blank=True, choices=[('homepage', 'homepage'), ('homepageContact', 'homepageContact'), ('aboutpage', 'aboutpage'), ('contactpage', 'contactpage'), ('careerpage', 'careerpage'), ('teampage', 'teampage'), ('seedFundingPage', 'seedFundingPage'), ('earlyFundingPage', 'earlyFundingPage'), ('growthFundingPage', 'growthFundingPage'), ('sellYourStartupPage', 'sellYourStartupPage'), ('sellESOPPage', 'sellESOPPage'), ('seedFundingSignupPage', 'seedFundingSignupPage'), ('earlyFundingSignupPage', 'earlyFundingSignupPage'), ('growthFundingSignupPage', 'growthFundingSignupPage'), ('sellYourStartupSignupPage', 'sellYourStartupSignupPage'), ('sellESOPSignupPage', 'sellESOPSignupPage'), ('privateBoutiquePage', 'privateBoutiquePage'), ('privateBoutiqueContactPage', 'privateBoutiqueContactPage'), ('preIPOPage', 'preIPOPage'), ('blogHomePage', 'blogHomePage'), ('videoBlogListPage', 'videoBlogListPage'), ('newsBlogListPage', 'newsBlogListPage'), ('stockListPage', 'stockListPage'), ('mediaListPage', 'mediaListPage'), ('videoShortsListPage', 'videoShortsListPage'), ('newsFeedListPage', 'newsFeedListPage'), ('articleListPage', 'articleListPage'), ('buyPreIPOPage', 'buyPreIPOPage'), ('channelPartnerPage', 'channelPartnerPage'), ('channelPartnerSignupPage', 'channelPartnerSignupPage'), ('offersPage', 'offersPage'), ('videoBlog', 'videoBlog'), ('shortsBlog', 'shortsBlog'), ('articleBlog', 'articleBlog'), ('newsBlog', 'newsBlog'), ('researchReports', 'researchReports')], max_length=256, null=True),
        ),
    ]
