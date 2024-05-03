import json
from rest_framework import serializers
from .models import categoryOptions, subCategoryOptions, blogVideos, blogVideoDetailedDM
from django.utils.html import strip_tags
from taggit.managers import TaggableManager


class categoryOptionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = categoryOptions
        fields = ('name',)


class subCategoryOptionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = subCategoryOptions
        exclude = ('author', 'publish', 'created', 'updated', 'status', 'description')


class blogVideosSerializer(serializers.ModelSerializer):
    class Meta:
        model = blogVideos
        exclude = ('author', 'created', 'updated', 'status', 'subTitle', 'content', 'blogVideo')


class blogVideosDetailedSerializer(serializers.ModelSerializer):
    tags = serializers.SerializerMethodField('get_tags')
    weburl = serializers.URLField(source='get_absolute_url', read_only=True)

    class Meta:
        model = blogVideos
        fields = ('id', 'title', 'slug', 'blogImage', 'blogVideo', 'videoLink', 'subTitle', 'content', 'excerptContent',
                  'category', 'tags', 'weburl')

    def get_tags(self, obj):
        tags = list(obj.tags.all().values())
        return tags
