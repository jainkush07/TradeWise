from rest_framework import serializers
from .models import blogNews, blogNewsListingDM, newsHeadingDM
from django.utils.html import strip_tags
from stockApp.models import stockBasicDetail


class LogoSerializer(serializers.ModelSerializer):
    class Meta:
        model = stockBasicDetail
        fields = ('logo',)


class blogNewsSerializer(serializers.ModelSerializer):
    researchReportForLogo = LogoSerializer()
    weburl = serializers.URLField(source='get_absolute_url', read_only=True)

    class Meta:
        model = blogNews
        exclude = ('author', 'created', 'updated', 'status', 'content2', 'content3', 'content4', 'content5')


class blogNewsListingDMSerializer(serializers.ModelSerializer):
    class Meta:
        model = blogNewsListingDM
        exclude = ('publish', 'created', 'updated', 'status')


class newsHeadingDMSerializer(serializers.ModelSerializer):
    class Meta:
        model = newsHeadingDM
        exclude = ('newsBlog', 'publish', 'created', 'updated', 'status')


from .models import *


class newsHeadingWebDMSerializer(serializers.ModelSerializer):
    class Meta:
        model = newsHeadingWebDM
        fields = '__all__'


class LogoSerializer(serializers.ModelSerializer):
    class Meta:
        model = stockBasicDetail
        fields = ('logo',)


class feedDescriptionSerializer(serializers.ModelSerializer):
    researchReportForLogo = LogoSerializer()

    class Meta:
        model = blogNews
        fields = ('title', 'created', 'researchReportForLogo', 'content1', 'content2', 'content3', 'content4',
                  'content5', 'imageUpload', 'pptForNews', 'timeOfNews')
