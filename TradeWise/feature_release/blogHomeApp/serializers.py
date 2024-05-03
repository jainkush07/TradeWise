from rest_framework import serializers
from taggit.models import Tag
from dmFormsApp.models import metaDetailForDM
from mediaBlogApp.models import blogMedia
from newsBlogApp.models import blogNews
from videoShortsApp.models import blogVideosShorts
from videoBlogApp.models import blogVideos
from articleBlogApp.models import blogArticles
from stockApp.models import stockBasicDetail


class stockBasicDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = stockBasicDetail
        fields = '__all__'


class blogArticlesSerializer(serializers.ModelSerializer):
    class Meta:
        model = blogArticles
        fields = '__all__'


class blogVideosSerializer(serializers.ModelSerializer):
    class Meta:
        model = blogVideos
        fields = '__all__'


class blogVideosShortsSerializer(serializers.ModelSerializer):
    class Meta:
        model = blogVideosShorts
        fields = '__all__'


class blogNewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = blogNews
        fields = '__all__'


class metaDetailForDMSerializer(serializers.ModelSerializer):
    class Meta:
        model = metaDetailForDM
        fields = '__all__'


class tagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'

class blogMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = blogMedia
        fields = '__all__'